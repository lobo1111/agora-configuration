from base.Container import Container
import re

class PaymentCalculator(Container):
    def capitalize(self, line):
        return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])
    
    def getAttributeValue(self, instance, attribute):
        result = getattr(instance, 'get' + self.capitalize(attribute))()
        if hasattr(result, 'floatValue'):
            return getattr(result, 'floatValue')()
        else:
            return result
    
    def calculate(self, element, possession):
        entities = {"element" : element, "possession" : possession}
        if possession is not None:
            entities['possessionData'] = possession.getAdditionalData()
        algorithm = element.getAlgorithm().getValue()
        occurences = re.findall('#\{(.+?)\.(.+?)\}', algorithm)
        for occurence in occurences:
            entity = occurence[0]
            attribute = occurence[1]
            print 'Looking for %s.%s' % (entity, attribute)
            instance = entities.get(entity)
            if instance is None:
                self._logger.info('Entity not found, assuming attribute value = 0')
                value = 0
            else:
                try:
                    value = self.getAttributeValue(instance, attribute)
                    self._logger.info('Value established = ' + str(value))
                except:
                    value = 0
                    self._logger.info('Exception raised, attribute not found(%s). Assuming attribute value = 0' % attribute)
            algorithm = algorithm.replace('#{' + entity + '.' + attribute + '}', str(value))
        algorithmValue = eval(algorithm)
        print str(algorithm) + '=' + str(algorithmValue)
        return algorithmValue