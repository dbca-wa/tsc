.. _data-capture:

============
Data capture
============

This chapter addresses data capture, who enter and maintain the data.

TSC's data model is built around an extended concept of AreaEncounter, which is
the physical encounter of an observer with individuals of a species (fauna or flora)
or an ecological community (threatened, priority, or neither) at a location.
The extent occupied by the species or community can be described either as a point
(animal location) or polygon (community boundary or plant population).
The encounter can incur any range of additional observations of the species or community,
the location, or the surroundings.

The following sections will instruct data entry operators how to enter data from
supported data sources into WAStD/TSC.

.. * link to example data sheets of all supported formats, and
.. * for each format, map the fields of the paper form to the online form.


Conservation Actions
====================
This section will explain business processes around Conservation Actions (CA).
CA counteract threats.
CA are suggested, may be liked to species, communities, documents, certain areas,
individual occurrences (survey sites, plant populations, community boundaries),
or any combination thereof.

.. Cons assets: thr and prio species and communities
.. Robyn Luu has cons actions




.. _itp-species-fauna:
Threatened Fauna Occurrence
===========================

Paper form
----------
This section discusses changes to the legacy paper form to streamline it for TSC use.

Audience: TSC stakeholders, Species and Communities Branch.

Form version: NA, long version

* Species ID: proof (photos, samples, text description), certainty of ID,
* Specimen: label, location
* Population Observation: number at age classes
* Survey: methodology, type
* Animal observation: secondary signs, cause of death, reproductive state
* Habitat: landform, veg type
* Fire history
* Associated flora species
* Associated communities

Digital form
------------
Needs a lot of thought to streamline the very different scenarios in which an animal occurrence might be recorded.


.. _itp-species-flora:
Threatened Flora Occurrence
===========================

Paper form
----------
This section discusses changes to the legacy paper form to streamline it for TSC use.

Audience: TSC stakeholders, Species and Communities Branch.

Form version: 1.1 Jan 2012

* DRF permit
* Area assessment
* Quadrats
* Population structure
* Population condition
* Threats
* Habitat information
* Habitat condition
* Fire history
* Vegetation classification
* Associated species



.. _itp-community:
Ecological Community Occurrence
===============================

TEC Occurrence Report Form
--------------------------
This section discusses changes to the legacy paper form to streamline it for TSC use.

Audience: TSC stakeholders, Species and Communities Branch.

Form version: 6.0 July 2013

Glossary
^^^^^^^^

* [A] Assumption
* [D] Derived information, can be reconstructed from other information, not required to capture. Exclude from paper form.
* [R] Redundant information, duplicates other information, not required to capture.
* [K] Keep, already implemented.
* [N] New, add.
* [X] Remove as per stakeholder advice.

Part 1: Encounter details
^^^^^^^^^^^^^^^^^^^^^^^^^
The "w"s: Who, when, where, what.

Section "Community":

* Community: [K][A] The data collector must know the community code.
* Observation date: [K] ``encountered_on``.
* New occurrence: [D]
* Observers: ``encountered_by`` is the primary observer. [A] Clearly associated responsibility of reported information and person reporting.
* Role, email, organisation: [D] already in TSC. [A] every data reporter is or will be registered as user in TSC.

Section "Submission":

* Person submitting record [A] is that person entering record in TSC?

Section "Location":

* Description of location: [R] hand-waving about location is replaced with polygon or point.
* District, LGA, Reserve no: [D]
* Land manager present: [N] - what other fields are included in "Land manager attendance"?
* Datum: [R] default is WGS84.
* Coodinates: [R] replaced by polygon / point map widgets.
* Method used: [R] replaced by ``location_accuracy``.
* Land tenure: [D]

Section "Area assessment" -- keep and migrate legacy data, no new form

* Type (edge, partial, full): [N] add as area types: TEC boundary (edge), TEC boundary (partial)
* Area observed (m2): [D] from polygon
* Effort: [D] from [N] survey start time / [N] survey end time
* Time spent per area: [D] from survey end - start time / area observed

Part 2: The occurrence
^^^^^^^^^^^^^^^^^^^^^^
Condition, composition, threats and mitigation.

Section "Condition of occurrence":

* Single group. [N]
* Percentage of occurrence being rated on the Bush Forever scale as Decimal(2,0):

  * Pristine
  * Excellent
  * Very good
  * Good
  * Degraded
  * Completely degraded

Fields must add up to 100.

Section "Associated species":
* Repeating group. [N] m2m to species.

Section "Threats": make compatible with IUCN criteria.


* Repeating group. [N]
* Threat [N] - category or free text?
* Cause / agent [X]
* Area affected percentage [N]
* Current impact severity [N] Nil, low, medium, high, extreme
* Potential impact severity [N] low, medium, high, extreme
* Potential threat onset [N] short term (whithin next 12 months), medium term (within 1-5 years), long term (after more than 5 years)

Section "Recommended management actions" & "Actions implemented":

* Repeating groups, correspond to area management actions (including reporting).

Part 3: Location
^^^^^^^^^^^^^^^^
Habitat, fire history.

Section "Habitat information": Add "other, see comments", "comments".

* Single group. [N]
* Land form: multiple select.
* Rock type: multiple select.
* Loose rock: [X], but keep legacy.
* Soil type: multiple select.
* Soil colour: multiple select.
* Drainage: single select.
* Specific landform element (see field manual) [X] but keep legacy.
* Soil condition -> rename as soil moisture: single select.
* Vegetation classification: [X] but keep legacy.

Section "Fire history":

* Single group. [N]
* Last fire (date)
* Fire intensity (high/medium/low)
* No evidence of fire


Part 4: Attachments and additional information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Section "Comments":

* Single group. [N]
* Text comments.

Section "Attachments"

* Repeating group.
* File, title, category.


TEC Bushland Plant Survey Recording Sheet
-----------------------------------------
* Encounter
* Location
* Habitat
* Veg structure and cover [R]

  * life form (trees over 30m, trees 10-30m, trees < 10m, mallees > 8m, mallees < 8m, ...)
  * cover class (select)
  * dominant species (m2m)
* Section "Condition of occurrence"
* Species presence observation

  * Taxon
  * Collecting ID: made up in the field, unique to collected specimen within survey
  * Reproductive state: flowering or not etc
  * Identified in the field or not




TSC data entry
--------------
This section explains how to use the TSC data entry forms.

Coming soon.

Plan:

* One form for each part.
* Common fields (as per "Taxon/Community Area Encounter") are the basic unit of an encounter with an occurrence.
* Additional groups are added as separate forms to the basic encounter.

Occurrences can be reported

* from the home page (any species or community),
* from a species or community detail page (the species or community is then already prefilled),
* from a species or community area, such as a flora (sub)population or a TEC boundary (area "code" which links occurrence to that area is then also prefilled).

Each occurrence has a detail page (coming soon), where additional data can be added (such as habitat information, fire history, etc).

