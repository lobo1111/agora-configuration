package pl.reaper.container.jms;

import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.annotation.Resource;
import javax.ejb.ActivationConfigProperty;
import javax.ejb.EJB;
import javax.ejb.MessageDriven;
import javax.jms.Destination;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.MessageProducer;
import javax.jms.QueueConnectionFactory;
import javax.jms.QueueSession;
import javax.jms.Session;
import javax.jms.TextMessage;
import pl.reaper.container.beans.JythonBeanLocal;

//@MessageDriven(mappedName = "jms/agoraQueue", activationConfig = {
//    @ActivationConfigProperty(propertyName = "acknowledgeMode", propertyValue = "Auto-acknowledge"),
//    @ActivationConfigProperty(propertyName = "destinationType", propertyValue = "javax.jms.Queue")
//})
public class RequestQueue implements MessageListener {

    private static final String SCRIPT_NAME = "SCRIPT_NAME";
    private static final String VARIABLES = "VARIABLES";
    @EJB
    private JythonBeanLocal jythonExecutor;
//    @Resource(mappedName = "jms/ConnectionFactory")
    QueueConnectionFactory connFactory;

    public RequestQueue() {
    }

    @Override
    public void onMessage(Message message) {
        try {
            String scriptName = message.getStringProperty(SCRIPT_NAME);
            Map variables = (Map) message.getObjectProperty(VARIABLES);
            String result = jythonExecutor.executeScript(scriptName, variables, true);
            sendResponse(message.getJMSMessageID(), message.getJMSReplyTo(), result);
        } catch (JMSException ex) {
            Logger.getLogger(RequestQueue.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void sendResponse(String messageId, Destination jmsReplyTo, String result) throws JMSException {
        QueueSession session = connFactory.createQueueConnection().createQueueSession(true,
                Session.DUPS_OK_ACKNOWLEDGE);
        MessageProducer replyProducer = session.createProducer(jmsReplyTo);
        TextMessage replyMessage = session.createTextMessage();
        replyMessage.setText(result);
        replyMessage.setJMSCorrelationID(messageId);
        replyProducer.send(replyMessage);
        session.close();

    }
}
