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
name, group, algorithm, default flag and global value. Algorithm is a parameterized
Python codevthat is parsed on-the-fly to calculate value.
2) Community level - if element on global level is flaged as 'default' then
for each newly created community CommunityElement is created and assigned to that
community. It's possible to add or remove(even default ones) CommunityElements
later.
3) Possession level - each CommunityElement existing on community is propagated
to newly created possession as PossessionElement. It's possible to add or 
remove(even default ones) PossessionElements later. Possession element doesn't
have to be bind to Community Element(!) - it can be created directly on Possession
level. In that case it's a two level structure.

PERSIST ALGORITHM:


ELEMENT VALUE EXTRACTION ALGORITHM:
Depends on provided element type. Value is extracted from the lowest level.
1) If provided element is of type PossessionElement:
    i) if override flag is set -> local element value is returned
    ii) otherwise go 'up' -> if PE is bound to CE switch to CE otherwise
        switch to GE
2) If provided element is of type CommunityElement:
    i) if override flag is set -> local element value is returned
    ii) otherwise go 'up' -> switch to GE
3) If provided element is of the Element:
    i) return local element value

ELEMENT ALGORITHM:
Each global level element is bound the an algorithm. Algorithm is a plain
Python code with variables pointed to application structure(Community and Possession).
On 'charge' action trigger it's used to calculate values for Charging document.

'''
class ElementManager(Container):
    
    '''
    It's a common method to create/update all kinds of elements(Element, 
    CommunityElement, PossessionElement). Mapper recognizes them based on provided 
    'type' variable(GLOBAL, COMMUNITY, POSSESSION).
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