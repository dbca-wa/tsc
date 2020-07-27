===============
Data collectors
===============

NOTE this chapter has been split up (content duplicated) into the data collection chapters for admins and collectors.





Each field in the data sheets has been, and should be questioned:

* Is this information used in any of the analytical outputs?
* Does this information serve any QA purpose?
* Is this information used to derive other information, e.g. deformities being
  used to identify a resighted, untagged animal?
* Will anyone in the foreseeable future require this information?

.. _data-capture-tracks:

Turtle tracks or nests
======================
Turtle track counts can be collected on mobile app (OpenDataKit, ODK),
or on paper data sheets (backup if ODK unavailable).

Tracks can be recorded individually (preferred) or tallied over beach sections.

* *Nest* counts: walking in a straight line along the high water mark, each
  uptrack is followed to its apex, where the presence or absence of a nest
  determines the type of track (track without nest, track with nest, track with
  a possible nest).
  If evident, nest disturbance is recorded as well.
  Disturbed unhatched nests without tracks, as well as hatched nests (without
  tracks), if spotted, are recorded as well.
* *Speed run* counts: walking in a straight line along the high water mark, only
  inbound tracks (uptracks) are counted as "tracks with success not assessed".
  The tracks are not followed. Except for the first day, only fresh (younger
  than 24h) tracks are recorded. Nests are recorded if spotted.
* *Track tallies* are recorded only under extreme time pressure, or on saturation
  beaches, where the geo-referencing of individual tracks is not possible within
  the available survey time. However, individual track counts (*nest* or *speed run*)
  are preferred.

Mobile data collection using Open Data Kit
------------------------------------------

Admin: First time setup
^^^^^^^^^^^^^^^^^^^^^^^
These steps have to be run once by the ODK admin per device while online.
Less than 10 MB will be downloaded.
These steps can also be run by an interested data collector on their own Android
device.

* On your Android device, install
  `ODK Collect <https://play.google.com/store/apps/details?id=org.odk.collect.android>`_
* In ODK Collect > General Settings > Server Settings > Configure platform settings:
* URL: https://dpaw-data.appspot.com, plus username and password as provided to
  you by the ODK admin. These credentials determine whether you can retrieve new
  forms and submit data, and the username will be automatically recorded when
  collecting data. It is crucial to spell the credentials exactly as provided.
* The username and password can also be set under General Settings > Server Settings.
* Auto send: "only with WiFi" if few data points are collected.
  Disable for vigorous data collection in remote areas with limited WiFi -
  don't swamp the WiFi hotspot by auto-uploading data with photos.
* Default to finalized
* Delete after send
* If the device is used by many volunteers who are new to the software, enable
  the "Admin Settings" (set password) and disable menu options that are not needed
  or risk data loss (e.g. "delete forms").

**Note** You **must not** share your credentials, and
**always use your own credentials** in General Settings > Username/Password
to collect data. Failure to do so **will** result in data loss, data corruption and
loss of attribution.


Admin: Prepare devices pre field trip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For each device before a field trip, while still within WiFi:

* Install ODK Collect, configure:
* server https://dpaw-data.appspot.com/
* username and password must be valid and spelled correctly
* Get Blank Forms > select latest "Track or Treat", "Track Tally", "Turtle Stranding"
* Delete Forms > Blank Forms > delete older versions of above forms

As discussed previously, it is possible to restrict user-accessible settings
to username / password only.
Do so at your own discretion (through Admin Settings) to reduce possible confusion
and user errors.

Collector: Prepare devices pre survey
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ideally, the admin handing out the Android device will double-check these settings
together with the data collector.

* **Credentials** Set the collector's ODK credentials (username and password)
  for the respective ODK Aggregate server, (e.g. https://dpaw-data.appspot.com/)
  **exactly** as given and **before** collecting data.
  The entered username will be stored automatically with each record (only
  correct usernames will ensure correct attribution), and used to authenticate
  data upload to ODK Aggregate (incorrect usernames will result in failed upload).
* **Battery** Make sure the battery is full before you head out.
  Screen and GPS are hungry hippos. Toggle WiFi and GPS depending on situation:
  GPS on only during surveys, WiFi on only during data upload.

**Note** Exact spelling includes capitalisation, interpunctuation and whitespace.
E.g., the username `stephen_king` is not correct if spelled `Stephen_King`,
`StephenK`, `stephen king`, `stephen-king` or `stephenking`.

.. image:: https://www.lucidchart.com/publicSegments/view/14429a0a-bc5c-4bbb-8bd1-527294874920/image.png
    :target: https://www.lucidchart.com/publicSegments/view/14429a0a-bc5c-4bbb-8bd1-527294874920/image.png
    :alt: Track Count work flow

Collector: Collect "speed run" data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Walk along the high water mark on the beach until you encounter either
  an unmarked inbound track ("uptrack") or unmarked outbound hatchling tracks.
* "Fill Blank Form" > Track or Treat (latest version)
* Track age: fresh (default) if less than 24 h old, or old if older than 24 h.
  If the beach was surveyed within the last day, all unmarked tracks are "fresh".
* Species: select species if possible, else if unsure, keep default "turtle".
* Take photo of track if unsure about species ID. Landscape format is preferred!
  Place a length reference (measuring tape) across the whole track, lining up
  the end with the edge of the track. This allows curators to gauge the track
  width easily from the photo.
  Select angle of camera, sun and track so that the track is clearly visible.

Adult turtle tracks:

* Track type: keep default "track, not checked for nest"
* Location: Start GeoPoint. Required. Can be saved as soon as "accuracy" is
  shown, will auto-save once accuracy drops below 5m. The fix should not take
  longer than 5 to 10 seconds. The acquisition speed depends on the device's GPS
  chip and available satellites. The first fix can take a bit longer, subsequent
  GPS fixes should be faster.

Hatchling tracks:

* Track type: "nest, hatched"
* Location: Follow to hatched nest, capture location of nest.
* Swipe right and fill in subsequent nest-related screens. A senior field worker
  will conduct the nest excavation.

You should at least set species and GeoPoint, if the other value defaults are correct.

Review the data, then swipe right to finish the form.

If you are sure of species ID, keep "Mark form as finalized" ticked and "Save Form and Exit".

If you are unsure of the species ID, (species is "turtle" and photo of track is
provided), untick "Mark form as finalized" and "Save Form and Exit".
This gives the field supervisors a chance to review and possibly determine species ID
(based on the photo taken) before uploading.

This form will take a trained operator about 13 taps and swipes over about 15 seconds
plus the time to take a photo.

Repeat for each track.

Collect "nest" data
^^^^^^^^^^^^^^^^^^^
Look for both tracks (crossing your path) and nests (may be inland).

**Track** same screen as uptrack up to photo of track. Resuming from track type:

* Follow the track until you find the nest or downtrack.
* Depending on presence of nest, set Track or nest type: "track without nest",
  "track with nest", or "track, checked for nest, unsure if nest".
* If you're unsure about the presence of a nest, take a photo of the nest and
  do not mark the record as "finalized". This gives the field supervisors a
  chance to review and possibly determine nesting success
  (based on the photo taken) before uploading.
* Record the location of the nest, or (if no nest found) the track apex.

**Nest** choose whether nest is unhatched (no shells) or hatched (shells).

Swipe right. If nest is present, fill in the "nest" screen.
Indicate whether:

* disturbance was evident,
* eggs were counted,
* the nest had an ID tag buried within the eggs (or tied to a nest marker pole),
* there was a temperature logger in the nest, or
* hatchlings were found and measured.

Swipe right. Depending on the indications above, extra screens will be shown.

**Disturbance**

* "Add a new Disturbance observation group" for each distinct disturbance cause.
* Record disturbances before excavating nests, take photos of evidence.

**Eggs**
This step assumes that a trained operator has now excavated the nest, and sorted
the eggs into the categories defined by Miller (1999) on top of a cutting board
with a reference grid.

* egg category tallies are required (0 if none found)
* nest depth (caution - millimeters) is optional
* photograph the eggs on top of the reference cutting board and take as many
  pictures as required.

**Nest tag**
Some nests may contain a nest tag, which consists of builders' ribbon with the
nest tag ID written in text marker on it.
A nest tag ID consists of up to three parts:

* Flipper tag ID: provide **exactly one**, and **do not** include any other information.
  e.g. `WA1234`. Whitespace and capitalisation will be ignored, so `wa1234`,
  `WA 1234` and `wa 1234` are equivalent. However, `WA1234 and some words` will
  **not** match up with flipper tag `WA1234` unless manually rectified.
  Operators are encouraged to enter this value with greatest care and precision.
  The turtle flipper tag may have been unavailable or unknown at the time of
  writing the nest tag, so it can be blank.
* Date nest laid: this is the **calendar** date of the nesting event. If a nest
  was tagged after the initial nesting event, the date may be unknown, and
  therefore also blank.
* Nest label: any extra information that is not the first flipper tag or the
  lay date will go here, e.g. an informal nest name like `M1`. The nest label
  may also be blank.

**Temperature logger**
In hatched nests, one or two temperature loggers can be found, and will always
be retrieved for later data download.

* Logger ID: the number underneath the bar code.
* Photo: take a photo of the logger ID / serial / bar code area if lighting allows.
  This is a good backup for proofreading the logger ID.
* Why not barcode: the white-on-black HOBO logger barcode does not scan quickly,
  and barcode scanners can mistakenly OCR the logger ID (from plain text).

**Hatchling measurement**
Enter straight carapace length in mm, straight carapace width in mm and weight in grams.

This is the end of the form. Proceed to the next track or nest and repeat.

At the end of the survey, turn off location services, and hand the device back to the admin.

Admin: Review data
^^^^^^^^^^^^^^^^^^
"Edit Saved Form" lists all unfinalized forms pending review and species / nest ID:

* Tap once to view read-only, tap again to edit
* review and update data (e.g. species ID)
* save and mark as finalized.


Admin: Upload data
^^^^^^^^^^^^^^^^^^
When surveys are done in locations where the device can return to the comforts
of WiFi and power points daily, data can be uploaded directly to the clearinghouse.

* Settings: make sure the correct username and password are given. The admin can
  choose to use their own username / password.
* Turn on the WiFi hotspot or move into WiFi range.
* Turn on the device's WiFi.

With "Auto-send in WiFi" settings enabled, the device will automatically upload
all data marked as "finalized".

When WiFi is not available daily, the admin needs to backup data by downloading
it manually and keeping the downloaded data safe (multiple copies over separate
storage media). With the mobile device connected and "MTP file transfer" enabled,
ODK data is located in either internal or SD storage in ``odk/instances``.
Each form will be stored in a separate folder, containing both the filled in form
as XML file, and all related pictures and media.

Where's the data now?
^^^^^^^^^^^^^^^^^^^^^
ODK Collect uploads data to the configured ODK Aggregate clearinghouse.
In our case, this is https://dpaw-data.appspot.com/.
Data collectors will have received credentials to login, which are the credentials
to be used in ODK Collect.

A synchronised copy of the data is streamed to Google Fusion Tables (GFT)
for immediate visualization.

For an initial analysis and summary, data are downloaded from GFT and presented
in an RMarkdown workbook `Tracks <http://rpubs.com/florian_mayer/tracks>`_.

After each field trip, data from ODK Aggregate are exported (as JSON) and ingested
into WAStD. The process can be repeated; data that has been changed in WAStD and
marked as "proofread" or even "curated" will not be overwritten.

Once data are marked as "proofread" (or higher levels of QA) in WAStD,
WAStD becomes the point of truth, as proofreading and curation (e.g.
double-checking species ID based on submitted photos) can change the data compared
to the initial submission on ODK Aggregate.

Once data is ingested into WAStD, it is visible and accessible to DPaW staff at
https://strandings.dpaw.wa.gov.au/. See chapter "Data consumers" for working
examples.

The final analysis (in development at the time of writing) will consume
curated data through the WAStD API.

.. _itp-stranding-report:

Turtle Stranding
================

Setup the device as described above and select the latest "Turtle Stranding" form
in "Get blank forms".

The expected work flow is:

* A member of the public reports a stranded animal, a field officer responds to
  the report and inspects the stranded animal personally.
* A field officer discovers a stranded animal during a patrol.
* In both cases, the field officer carries a mobile device with ODK Collect and
  the latest "Turtle Stranding" form.
* The field officer fills in the form while attending to the stranded animal.
* All freshly dead turtles (D1 and D2) should be frozen and sent to Perth
  (Erina Young) for a necropsy.

The form should be self-explanatory. Some fields default to the "not assessed / NA"
option, however effort should be untertaken to determine the correct option.

Photographs are very important, in that they allow data curators to verify the field
operator's choice of available options.

If possible, photographs should be taken in landscape format.

The habitat photo should be taken from about 10 m distance to the animal.

Although taking several photos next to a decomposing animal may pose an olfactory
challenge, taking a photo is invaluable, in that it cannot be taken at a later
time, and it preserves valuable and volatile information.


.. _lessons-learnt-paper-based-data-capture:

Lessons learnt from paper-based field data collection
=====================================================

Scenario 1: Two tags applied, both tags recorded incorrectly
------------------------------------------------------------
One turtle is encountered in two subsequent nights by two separate teams.

Night 1
^^^^^^^
* Data entry operators "Tim" and "Natalie" were in a rush, tagged turtle with tag "WB7326", but
  recorded next tag "WB7330" on tag dispenser as "applied new".
* Operators grabbed a PIT tag "900006000144755" from bag and applied it to turtle,
  then went back to the bag, mistook another empty PIT package of tag
  "900006000143470" (hint: with a few missing ID stickers - missing means peeled
  off by sand, or stuck onto another datasheet when applied to a turtle)
  for the package of the just applied tag "...755" and recorded "...470" incorrectly
  as "applied new".
* Team 1 measure CCL

Night 2
^^^^^^^
* Second team "Spud" and "Coral" encounter the same turtle with left flipper tag
 "WB7326"
* They scan for PIT tag, find and record "...755"
* They apply and record another flipper tag "WB7384" on right flipper
* They measure CCL and CCW

The aftermath
^^^^^^^^^^^^^
* Team leader "Spud" wants to lookup tag history "WB7326", suspecting the turtle
  might originate from different nesting location, based on the fact that the
  turtle was already tagged. Most likely, seeing a tagged turtle this early in the
  tagging season means that the tag has been applied elswhere earlier.
* The tag is not in the tagging database. This is unexpected.
* Data curator realises that the tag is from the tag series allocated to the current
  field trip. This means that the tag must have been applied new within the past
  days, and the corresponding datasheet must be present in the field office.
* Data curator spends the next half hour manically trying to find the datasheet
  referencing the application of tag "WB7326".
* Data curator questions correctness of first datasheet's tag ID.
* Day 1's datasheet is the only potentially matching candidate with similarities
  to day 2's datasheet: CCL within 3mm, one tag on front left flipper.
* Data curator decides that at least one of two datasheets is incorrect.
* Data curator locates "WB7330" in one of the tagging backpacks. This means that
  datasheet 1's flipper tag ID must be incorrect.
* Data curator infers based on similar body length and position of single flipper
  tag, datasheet 1 and 2 refer to the same turtle, and corrects the tag ID on
  datasheet 1 to "WB7326".
* Data curator learns from "Natalie" that the empty PIT tag box had only two
  remaining stickers out of five left. This indicates that the recorded PIT tag ID
  on datasheet 1 is also incorrect. The curator therefore assumes that the PIT
  tag ID of datasheet 2 is correct and adjusts datasheet 1 to report PIT tag ID
  "...755".

Lessons learnt from mobile field data collection
================================================

The choice of methodology can be driven by time availability.

Example: Teams are dropped off on remote beaches and have too little time to
identify and individually record turtle tracks (on paper or on mobile).
In this case, a tally was kept on paper forms, as no specialised mobile app for
tally observations was available yet.

Devices shoot-out
-----------------
Hands-on field testing at Thevenard and Barrow Islands Nov/Dec 2016.

General notes
^^^^^^^^^^^^^
* There are not many rugged cases available for low end, older or exotic devices
* $70 charger with 6 USB outlets replaces the Great Charger Kelp Forest
* $80 15Ah battery packs provide backup power
* $5 neoprene sleeves protect every device against bumps, scratches and sand
* $5 whiteboards plus whiteboard marker, placed in geotagged photo of any random
  observation are the best way to capture opportunistic observations

Samsung Galaxy S2 9.7"
^^^^^^^^^^^^^^^^^^^^^^
* $700 device, $150 rugged case, $50 64GB SD
* Office sleeves available in store, rugged cases only available online
* GPS fix ~ 10 sec to below 5m accuracy
* 64 GB internal storage is plenty for data collection
* Battery life excellent
* Screen excellent resolution and daylight readability
* System fast and snappy
* Android 6.0.1
* Large size is excellent to review visualisations and read
* (-) Larger size (A4 page) requires two hands to hold
* (-) too expensive to distribute widely or use in extreme conditions

Samsung Galaxy S2 8"
^^^^^^^^^^^^^^^^^^^^
* $550 device, $150 rugged case, $50 64GB SD
* Fits in 8" sleeve, can be balanced on one hand while operating with other.
* Same pros and cons as 9.7" version, plus:
* Size is on the border of one and two hand hold (depending on hand size).
* 32 GB internal storage is still plenty for data collection.
* (-) still too expensive to distribute widely or use in extreme conditions.

Samsung Galaxy Tab A 7"
^^^^^^^^^^^^^^^^^^^^^^^
* $160 device, $30 plastic shell, $50 64GB SD
* Fits in 7" sleeve, large trouser pocket, can be held securely in one hand.
* Rugged cases available in store at time of writing.
* Decidedly slower and laggier performance than flagship S2.
* (-) GPS unacceptably slow.
* (-) 8GB internal storage is too small to collect data.
* (-) Android 5.1.1 means external SD chip does not format as internal storage.

Lenovo Tab 3 7" TB3-730F
^^^^^^^^^^^^^^^^^^^^^^^^
* $100 device, $50 64GB SD
* No cover in store, but device is splash-resistant.
* Fits in 7" sleeve, trouser pocket, can be held securely in one hand.
* Very fast GPS fix, faster than Samsung S2, slower than a Moto G4+ phone.
* Best cost-benefit for handing out in bulk.

Moto G4 Plus phone
^^^^^^^^^^^^^^^^^^
* $400 device, $4 plastic shell, $50 SD
* Very good mid-range 5" Android phone
* Fast GPS fix (~4-5 sec outdoors)
* Dual SIM
* Data collection works nicely
* Good option for work phone for front-line staff at time of writing (Dec 2016)


General observations
^^^^^^^^^^^^^^^^^^^^
* All devices were daylight-readable.
* All devices had sufficient battery life to support hours of data collection.
* Operation in harsh environments was no problem: walking along sandy beaches in
  daylight, sweaty fingers, flying sand.
* External battery packs extend time between wall power charging.
* Best low-cost field device: Lenovo Tab 3. Runner-up: Samsung S2 8".
* Strong case against Galaxy Tab A (slow GPS, low internal storage, old OS version).


.. _cost-benefit-analysis-digital-data-capture:

Cost-benefit analysis for digital data collection
=================================================

The following diagram is also shown at :ref:`dm-data-entry`.

.. image:: https://www.lucidchart.com/publicSegments/view/e903e543-e5b9-4b4e-b05f-035772f5bb36/image.png
    :target: https://www.lucidchart.com/publicSegments/view/e903e543-e5b9-4b4e-b05f-035772f5bb36/image.png
    :alt: Turtle data flow, ideal state

Digital data collection provides systematic advantages over paper-based
data collection, as it skips several work-intensive, error-prone steps
in the data life cycle.

Paper-based data collection
---------------------------

Filling in a paper data sheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Error sources: typos, illegible or rushed handwriting, invalid values, fields
  incorrectly filled or skipped.
* Breaking the analog-digital barrier multiple times is costly and error prone:
  GPS, PIT tag reader, barcodes for samples etc.
* Associating media to records is labourious and error-prone

Digitising a paper data sheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Data collected on paper has to be read (interpreting handwriting correctly),
mentally mapped from datasheet to electronic form, and typed off (correctly) by
the data entry operator.

Proof-reading a digital record against paper data sheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A second person, acting as proofreader, has to reproduce the same mental effort
to map the paper data sheet to the electronic form and correct any errors they find.


Digital data collection
-----------------------
Digital forms can offer dropdown menus with pre-defined values to reduce sources
of error.

Digital data capture devices can reliably and easily record and associate
location and take photos. Compare pressing a "record location" button to taking
a GPS point, reading, understanding, typing, and confirming 15 digits under time
pressure, sleep deprivation and harsh environmental conditions.

Data collected digitally enters the system as "proofread", eliminating two laborious
and error-prone steps requiring human interaction.
In addition, the data is available to QA straight away, possibly creating a
tighter error-checking loop.