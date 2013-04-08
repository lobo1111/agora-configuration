package pl.reaper.container.beans;

import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.script.ScriptException;
import pl.reaper.container.data.Script;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptEngineWrapper;
import pl.reaper.container.jython.ScriptExecutor;
import pl.reaper.container.jython.ScriptLoader;

@Stateless
public class ScriptCompilator implements ScriptCompilatorLocal {

    @PersistenceContext(name = "agora_erp", unitName = "agora_erp")
    private EntityManager entityManager;

    @Override
    public Object compile(ScriptEngineWrapper engineBuilder, String scriptName, Map variables) {
        try {
            List<Script> chain = getScriptLoader().loadScriptChain(scriptName);
            engineBuilder.addVariables(variables);
            for (Script script : chain) {
                engineBuilder.addVariable("_scriptId", script.getId());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Initializing script {0}...", script.getName());
                engineBuilder.eval(script.getScript());
                Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Script {0} initialized.", script.getName());
            }
            Logger.getLogger(ScriptExecutor.class.getName()).log(Level.INFO, "Executing final script...");
            return engineBuilder.eval(chain.get(chain.size() - 1).getOnInit());
        } catch (ScriptException ex) {
            Logger.getLogger(ScriptCompilator.class.getName()).log(Level.SEVERE, engineBuilder.getLastExecuted(), ex);
            return null;
        }
    }

    private ScriptLoader getScriptLoader() {
        ScriptLoader scriptLoader = new DBScriptLoader(entityManager);
        return scriptLoader;
    }
}
