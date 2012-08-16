package pl.reaper.container.beans;

import com.kenai.crontabparser.CronTabExpression;
import java.text.ParseException;
import java.util.Calendar;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.Schedule;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import org.eclipse.persistence.queries.ScrollableCursor;
import pl.reaper.container.data.ScriptScheduler;
import pl.reaper.container.jython.DBScriptLoader;
import pl.reaper.container.jython.ScriptExecutor;

@Stateless
public class Cron implements CronLocal {

    @PersistenceContext
    private EntityManager entityManager;

    @Schedule(minute = "*", second = "0", dayOfMonth = "*", month = "*", year = "*", hour = "*", dayOfWeek = "*")
    public void myTimer() {
        Logger.getLogger(Cron.class.getName()).log(Level.INFO, "Timer fired, checking script scheduler...");
        ScrollableCursor cursor = loadScripts();
        while (cursor.hasMoreElements()) {
            ScriptScheduler scriptScheduler = (ScriptScheduler) cursor.next();
            if (shouldFire(scriptScheduler)) {
                executeScript(scriptScheduler);
            }
        }
        Logger.getLogger(Cron.class.getName()).log(Level.INFO, "Timer fired, all scripts checked.");
    }

    public ScrollableCursor loadScripts() {
        Query query = entityManager.createQuery("SELECT s FROM ScriptScheduler s WHERE s.enabled = true");
        query.setHint("eclipselink.cursor.scrollable", true);
        return (ScrollableCursor) query.getSingleResult();
    }

    private boolean shouldFire(ScriptScheduler scriptScheduler) {
        boolean result = false;
        try {
            Calendar today = Calendar.getInstance();
            CronTabExpression expression = CronTabExpression.parse(scriptScheduler.getSchedule());
            result = expression.matches(today);
            Logger.getLogger(Cron.class.getName()).log(Level.INFO, "Script scheduler({0}) activation result - {1}", new Object[]{scriptScheduler.getName(), result});
        } catch (ParseException ex) {
            Logger.getLogger(Cron.class.getName()).log(Level.SEVERE, null, ex);
        }
        return result;
    }

    private void executeScript(ScriptScheduler scriptScheduler) {
        ScriptExecutor executor = new ScriptExecutor(new DBScriptLoader(entityManager), entityManager);
        executor.prepareAndExecuteScript(scriptScheduler.getScript().getName());
    }
}
