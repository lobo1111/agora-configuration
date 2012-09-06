package pl.reaper.container.jython;

public class ScriptEngineNotFoundException extends Exception {

    ScriptEngineNotFoundException(String name) {
        super("Script not found: " + name);
    }
    
}
