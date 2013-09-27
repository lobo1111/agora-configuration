package pl.reaper.container.jython;

import java.util.HashMap;
import java.util.Map;
import javax.script.CompiledScript;

public class ScriptCache {

    private static Map<String, CompiledScript> cache = new HashMap<>();

    public static CompiledScript getFromCache(String scriptName) {
        return cache.get(scriptName);
    }

    public static void cache(String scriptName, CompiledScript script) {
        cache.put(scriptName, script);
    }
}
