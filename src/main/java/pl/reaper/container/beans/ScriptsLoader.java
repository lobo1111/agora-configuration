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
import org.python.core.Py;
import org.python.core.PySystemState;

@Startup
@Singleton
@ConcurrencyManagement(ConcurrencyManagementType.CONTAINER)
public class ScriptsLoader implements ScriptsLoaderLocal {

    private Map<String, CompiledScript> scripts = new HashMap<>();
    private final String instanceRoot = System.getProperty("com.sun.aas.instanceRoot");
    private final String scriptsPath = instanceRoot + File.separator + "container" + File.separator + "scripts";

    @PostConstruct
    @Override
    public void compileScripts() {
        ScriptEngine engine = createEngine();
        Compilable compilingEngine = (Compilable) engine;
        for (File file : findAllScripts()) {
            try {
                Logger.getLogger(ScriptsLoader.class.getName()).log(Level.INFO, "Compiling script: {0}", file.getAbsolutePath());
                String name = file.getAbsolutePath().substring(scriptsPath.length() + 1, file.getAbsolutePath().length() - 3);
                CompiledScript script = compilingEngine.compile(new FileReader(file));
                scripts.put(name, script);
                Logger.getLogger(ScriptsLoader.class.getName()).log(Level.INFO, "Script compiled: {0}", name);
            } catch (FileNotFoundException | ScriptException ex) {
                Logger.getLogger(ScriptsLoader.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    @Lock(LockType.READ)
    @Override
    public CompiledScript getScript(String name) throws Exception {
        return scripts.get(name);
    }

    private ScriptEngine createEngine() {
        PySystemState engineSys = new PySystemState();
        engineSys.path.append(Py.newString(scriptsPath));
        Py.setSystemState(engineSys);
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("python");
        if (engine == null) {
            throw new IllegalStateException("Python engine not found. Make sure jython jar is loaded.");
        } else {
            return engine;
        }
    }

    private Iterable<File> findAllScripts() {
        List<File> files = new ArrayList<>();
        Logger.getLogger(ScriptsLoader.class.getName()).log(Level.INFO, "Looking for scripts in : {0}", scriptsPath);
        Path path = FileSystems.getDefault().getPath(scriptsPath);
        try (DirectoryStream<Path> ds = Files.newDirectoryStream(path, "*.py")) {
            for (Path file : ds) {
                files.add(file.toFile());
            }
        } catch (IOException ex) {
            Logger.getLogger(ScriptsLoader.class.getName()).log(Level.SEVERE, null, ex);
        }
        return files;
    }
}
