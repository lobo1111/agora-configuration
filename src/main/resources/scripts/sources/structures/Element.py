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
Element usaes 4 mappers. Global, Community, Possession and one to agregate them.
It's necessary because element can be created or edited on three levels.
1) Global level - handled by GlobalMapper. It's possible to update all attributes
at edition time. Changes will affect all children 1
2) Community level - Creating new entity on community level is possible with
attaching it to existing global element or can create two elements - one on
global level and one on community level. In case of found existing global element
only two attributes are available for edition: override global value and local value.
Other attributes are loaded too but not possible to edit. They are there just
for information. In case user wants to create a new element, it is possible
to use edit form on community level to provided data for new global element
and community element. In that case all field are available for edition.
* In case that user will provide name of existing element(but won't load it !)
it will be still possible to edit other attributes but persist algorithm will
ignore those changes and attach community element to existing global element.
3) Possession level - TODO

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

    def remove(self):
        mapper = ElementMapper()
        mapper.initStructure()
        self.removeEntity(mapper.getEntity())
    
    '''
    For given community creates default Community Elements based on Element
    entity configuration - every Element marked as 'default' will added
    to community as Community Element. That method is executed only for newly
    created communities.
    '''
    def createDefaultElementsForCommunity(self, community):
        DefaultElementsHelper().createDefaultElementsForCommunity(community)
    
    '''
    For given possession cascades current set of elements from community of that
    possession
    '''
    def createDefaultElementsForPossession(self, possession):
        DefaultElementsHelper().createDefaultElementsForPossession(possession)
        
    '''
    Helper method for obtaining value of the element. Entity provided in parameter
    can be ont of three types(Global, Community or Possession). ValueHelper
    recognizes it and provides current value based on 'override' flags on each level.
    '''
    def getValue(self, element):
        return ValueHelper().getValue(element)