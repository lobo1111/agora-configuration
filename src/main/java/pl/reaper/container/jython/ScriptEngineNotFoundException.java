package pl.reaper.container.jython;

class ScriptEngineNotFoundException extends Exception {

    ScriptEngineNotFoundException(String name) {
        super("Script not found: " + name);
    }
    
}
