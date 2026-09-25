
import importlib
import sys
from types import ModuleType


def loaded_modules() -> dict[str, ModuleType]:
    """ Return loaded modules belonging to icarus_dcc. 
    
    Returns
    -------
    dict[str, ModuleType]
        Mapping of fully qualified module names to loaded module objects.
        
    Notes
    -----
    Only includes ``icarus_dcc`` and its submodules already present in
    ``sys.modules``. Does not import or reload modules.
    """

    modules = {}
    
    for name, module in tuple(sys.modules.items()):
        if not isinstance(module, ModuleType):
            continue
        
        if name == 'icarus_dcc' or name.startswith('icarus_dcc.'):
            modules[name] = module
            
    return modules

def module_dependencies(module: ModuleType) -> set[str]:
    """ Return project modules directly referenced by a module.
    
    Parameters
    ----------
    module : ModuleType
        Module whose global namespace will be inspected.
        
    Returns
    -------
    set[str]
        Fully qualified names of referenced Icarus DCC modules,
        excluding the inspected module itself
    
    Notes
    -----
    Detects module objects stored in the modules global namespace.
    Does not detect dependencies represented only by imported classes,
    functions, or dynamically resolved references.
    """
    
    dependencies = set()
    
    for value in tuple(vars(module).values()):
        if not isinstance(value, ModuleType):
            continue
        
        name = value.__name__
        
        if name == module.__name__:
            continue
        
        if name == 'icarus_dcc' or name.startswith('icarus_dcc.'):
            dependencies.add(name)
            
    return dependencies

def dependency_order(
    modules: dict[str, ModuleType]
) -> tuple[str, ...]:
    """ Order modules so dependencies appear before their consumers.
    
    Parameters
    ----------
    modules : dict[str, ModuleType]
        Mapping of fully qualified module names to module objects.
        
    Returns
    -------
    tuple[str, ...]
        Module names ordered with detected dependencies first.
        
    Raises
    ------
    ValueError
        If a cycle is found among the detected dependencies.
        
    Notes
    -----
    Only dependencies present in ``modules`` are considered.
    Dependency detection uses ``module_dependencies`` and inherits 
    its limitations.
    """
    
    ordered = []
    visiting = set()
    visited = set()
    
    def visit(name: str) -> None:
        if name in visited:
            return
        
        if name in visiting:
            raise ValueError(
                f'Circular module dependency detected at "{name}".'
            )
            
        visiting.add(name)
        
        dependencies = module_dependencies(modules[name])
        
        for dependency in sorted(dependencies):
            if dependency in modules:
                visit(dependency)
                
        visiting.remove(name)
        visited.add(name)
        ordered.append(name)
        
    for name in sorted(modules):
        visit(name)
        
    return tuple(ordered)

def reload_loaded_modules() -> tuple[str, ...]:
    """ Reload loaded Icarus DCC modules in dependency order.
    
    Returns
    -------
    tuple[str, ...]
        Fully qualified names of successfully reloaded modules, in reload 
        order.

    Raises
    ------
    ValueError
        If a cycle is found among the detected module dependencies.

    Notes
    -----
    Modules that have not been imported are skipped. Existing instances
    retain their original class definition and should be recreated after
    reloading.
    
    Reloading stops if a module raises an exception. Modules reloaded
    before the failure remain updated; changes are not rolled back.
    
    This function does not unload or re-register Maya plugins.
    
    The reload helper itself is excluded from the reload batch.
    """
    
    importlib.invalidate_caches()
    
    modules = loaded_modules()
    modules.pop(__name__, None)
    
    names = dependency_order(modules=modules)
    reloaded = []
    
    for name in names:        
        importlib.reload(module=modules[name])
        reloaded.append(name)
        
    return tuple(reloaded)