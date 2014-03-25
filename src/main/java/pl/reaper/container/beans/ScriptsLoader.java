package pl.reaper.container.beans;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.PostConstruct;
import javax.ejb.ConcurrencyManagement;
import javax.ejb.ConcurrencyManagementType;
import javax.ejb.Lock;
import javax.ejb.LockType;
import javax.ejb.Singleton;
import javax.ejb.Startup;
import javax.script.Compilable;
import javax.script.CompiledScript;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;

@Startup
@Singleton
@ConcurrencyManagement(ConcurrencyManagementType.CONTAINER)
public class ScriptsLoader implements ScriptsLoaderLocal {

    private Map<String, CompiledScript> scripts = new HashMap<>();

    @PostConstruct
    @Override
    public void init() {
        ScriptEngine engine = createEngine();
        Compilable compilingEngine = (Compilable) engine;
        for (String path : findAllScripts()) {
            try {
                String name = path.substring(path.lastIndexOf(File.separator + 1));
                CompiledScript script = compilingEngine.compile(new FileReader(new File(path)));
                scripts.put(name, script);
                Logger.getLogger(ScriptsLoader.class.getName()).log(Level.INFO, "Script compiled: {0}", name);
            } catch (FileNotFoundException | ScriptException ex) {
                Logger.getLogger(ScriptsLoader.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    @Lock(LockType.READ)
    @Override
    public CompiledScript getScript(String name) {
        return scripts.get(name);
    }

    private ScriptEngine createEngine() {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new IllegalStateException("Python engine not found. Make sure jython jar is loaded.");
        } else {
            return engine;
        }
    }

    private Iterable<String> findAllScripts() {
        List<String> files = new ArrayList<>();
        Path path = FileSystems.getDefault().getPath("container" + File.separator + "scripts");
        try (DirectoryStream<Path> ds = Files.newDirectoryStream(path, "*.py")) {
            for (Path file : ds) {
                files.add(file.toFile().getAbsolutePath());
            }
        } catch (IOException ex) {
            Logger.getLogger(ScriptsLoader.class.getName()).log(Level.SEVERE, null, ex);
        }
        return files;
    }
}
