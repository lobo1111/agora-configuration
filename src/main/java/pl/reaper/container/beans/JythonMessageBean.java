package pl.reaper.container.beans;

import javax.annotation.Resource;
import javax.ejb.ActivationConfigProperty;
import javax.ejb.EJB;
import javax.ejb.MessageDriven;
import javax.ejb.MessageDrivenContext;
import javax.jms.Message;
import javax.jms.MessageListener;
import javax.jms.ObjectMessage;

@MessageDriven(
   name = "jms/jython-script",
   activationConfig = {
      @ActivationConfigProperty( propertyName = "destinationType", 
                                 propertyValue = "javax.jms.Queue"),
      @ActivationConfigProperty( propertyName = "destination", 
                                 propertyValue ="jms/jython-script")
   }
)
public class JythonMessageBean implements MessageListener {
 
   @Resource
   private MessageDrivenContext mdctx;  
 
   @EJB
   JythonBeanRemote jythonBean;
 
   @Override
   public void onMessage(Message message) {
      ObjectMessage objectMessage = null;
      objectMessage = (ObjectMessage) message;       
   }   
}