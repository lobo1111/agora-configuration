from base.Container import Container
from structures.helpers.element.DefaultElementsHelper import DefaultElementsHelper
from structures.helpers.element.Mapper import ElementMapper
from structures.helpers.element.ValueHelper import ValueHelper
from structures.validators.common.ValidationError import ValidationError

'''
ELEMENT HIERARCHY:

Elements are essentials for calculating rent values for possessions. It's
a three level structure. 
1) Global level - elements on that level aren't bound to any community and possession.
It's a root structure for two lower levels. It holds all essentials informations:
name, group, algorithm, default flag and global value. Algorithm is a parametriez Python code
that is parsed on-the-fly to calculate value.
2) Community level - if element on global level is flaged as 'default' then
for each newly created community CommunityElement is created and assigned to that
community. It's possible to add or remove(even default ones) CommunityElements
later.
3) Possession level - each CommunityElement existing on community is propagated
to newly created possession as PossessionElement. It's possible to add or 
remove(even default ones) PossessionElements later.

ELEMENT VALUE EXTRACTION ALGORITHM:


ELEMENT ALGORITHM:
'''
class ElementManager(Container):
    
    '''
    It's a common method to create/update all kinds of elements(Element, 
    CommunityElement, PossessionElement). Mapper recognizes them based on provided 
    'type' variable(GLOBAL, COMMUNITY, POSSESSION). After initialization - which
    is creating new structure or update of existing one - mapper updates its
    attributes. In case of element every field can be changed.
    '''
    def persist(self):
        try:
            mapper = ElementMapper()
            mapper.initStructure()
            mapper.setData()
            self.saveEntity(mapper.getEntity())
        except ValidationError, error:
            self.setError(error)

    '''
    For given community creates default Community Elements based on Element
    entity configuration - every Element marked as 'default' will added
    to community as Community Element. That method is executed only for newly
    created communities.
    '''
    def createDefaultElementsForCommunity(self, community):
        DefaultElementsHelper().createDefaultElementsForCommunity(community)
        
    '''
    Helper method for obtaining value of the element. Entity provided in parameter
    can be ont of three types(Global, Community or Possession). ValueHelper
    recognizes it and provides current value based on 'override' flags on each level.
    '''
    def getValue(self, element):
        return ValueHelper().getValue(element)