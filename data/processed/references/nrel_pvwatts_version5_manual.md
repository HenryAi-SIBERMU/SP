![image 1](<nrel_pvwatts_version5_manual_images/imageFile1.png>)

# PVWatts Version 5 Manual

### Aron P. Dobos

NREL is a national laboratory of the U.S. Department of Energy Office of Energy Efficiency & Renewable Energy Operated by the Alliance for Sustainable Energy, LLC

This report is available at no cost from the National Renewable Energy Laboratory (NREL) at www.nrel.gov/publications.

Technical Report NREL/TP-6A20-62641 September 2014

![image 2](<nrel_pvwatts_version5_manual_images/imageFile2.png>)

# PVWatts Version 5 Manual

### Aron P. Dobos

##### Prepared under Task No. SS13.5030

NREL is a national laboratory of the U.S. Department of Energy Office of Energy Efficiency & Renewable Energy Operated by the Alliance for Sustainable Energy, LLC

This report is available at no cost from the National Renewable Energy Laboratory (NREL) at www.nrel.gov/publications.

National Renewable Energy Laboratory 15013 Denver West Parkway Golden, CO 80401 303-275-3000 • www.nrel.gov

Technical Report NREL/TP-6A20-62641 September 2014

###### NOTICE

This report was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or any agency thereof.

This report is available at no cost from the National Renewable Energy Laboratory (NREL) at www.nrel.gov/publications.

Available electronically at http://www.osti.gov/scitech Available for a processing fee to U.S. Department of Energy and its contractors, in paper, from:

U.S. Department of Energy Office of Scientific and Technical Information P.O. Box 62 Oak Ridge, TN 37831-0062 phone: 865.576.8401 fax: 865.576.5728 email: mailto:reports@adonis.osti.gov

Available for sale to the public, in paper, from:

U.S. Department of Commerce National Technical Information Service 5285 Port Royal Road Springfield, VA 22161 phone: 800.553.6847 fax: 703.605.6900 email: orders@ntis.fedworld.gov online ordering: http://www.ntis.gov/help/ordermethods.aspx

Cover Photos: (left to right) photo by Pat Corkery, NREL 16416, photo from SunEdison, NREL 17423, photo by Pat Corkery, NREL 16560, photo by Dennis Schroeder, NREL 17613, photo by Dean Armstrong, NREL 17436, photo by Pat Corkery, NREL 17721.

NREL prints on paper that contains recycled content.

## PVWatts Version 5 Manual

Aron P. Dobos September 4, 2014

Abstract

The NREL PVWatts ® R calculator is a web application developed by the National Renewable Energy Laboratory (NREL) that estimates the electricity production of a gridconnected photovoltaic system based on a few simple inputs. PVWatts combines a number of sub-models to predict overall system performance, and includes several built-in parameters that are hidden from the user. This technical reference manual describes the sub-models, documents hidden parameters and assumptions for default values, and explains the sequence of calculations that yield the ﬁnal system energy production estimate. This reference applies to the signiﬁcantly revised version of PVWatts released by NREL in 2014.

Keywords: photovoltaics, PVWatts, systems modeling, solar analysis

- 1


#### Introduction and History

PVWatts is a popular web application for estimating the energy production of a grid-connected photovoltaic (PV) system. It is designed to be simple to use and understand for non-experts and more advanced users alike. PVWatts hides much of the complexity of accurately modeling PV systems from the user by making several assumptions about the type, conﬁguration, and operation of the system. Consequently, the results should be interpreted as being a representative estimate for a similar actual system operating in a year with typical weather. The errors may be as high as ± 10 % for annual energy totals and ± 30 % for monthly totals for weather data representing long-term historical typical conditions. Actual performance in a speciﬁc year may deviate from the long-term average up to ± 20 % for annual and ± 40 % for monthly values.

PVWatts has been online since 1999, and the original algorithms in version 1 were largely based on the approach of the Sandia PVFORM tool developed in the 1980s. A technical reference manual for PVWatts version 1 is available in [1]. Since then, several versions of PVWatts have been made available, though the system performance calculations have remained largely the same as version 1. The version history is shown in Table 1.

In 2013, NREL began the process of revamping the PVWatts online web application to update the visual appeal and functionality, consolidate versions to reduce the ongoing maintenance burden, and update the energy prediction algorithms to be in line with the actual performance of modern photovoltaic systems.

While PVWatts is a useful tool for obtaining a quick estimate of energy production from a photovoltaic system, several more sophisticated tools are available for making more accurate predictions. The System Advisor Model (SAM) is a free desktop application developed by NREL that allows users to model PV systems in much greater detail [4]. SAM also includes detailed economic analysis for residential, commercial, and utility-scale systems, as well as performance models for concentrating solar power (CSP), wind, solar water heating, and geothermal systems.

Table 1. Version History

Version Description Weather Data Options Date Status V1 Original online calculator. 239 TMY2 sites. Added 1998 Retiring

360 international sites in in 2014 2005.

V2 Modiﬁed to utilize a gridded 40 km Monthly 40-km gridded ir­ 2001 Retiring monthly weather data in the continen­ radiance & temperature in 2014 tal US. Hourly calculations were done (CSR) with the nearest TMY2 site, and then the monthly totals were scaled using the monthly gridded weather data.

SOAP A web service version of V2 using Same as V2 2003 Retiring the SOAP protocol for monthly predic­ in 2014 tions.

- V3 Web service version of the hourly NREL/Clean Power 2009 Defunct PVWatts V1 using the 10-km hourly Research Perez 10-km in 2012 satellite-based irradiance dataset. In­ satellite-based irradiance, cluded a simpliﬁed economic cash ﬂow typical ﬁles created from calculation. 1998-2005 period of record
- V4 Updated REST-ful web service 239 TMY2s, 1020 TMY3s, 2012 Operational


of the hourly PVWatts V1 on 360 International, 10 km http://developer.nrel.gov CPR/Perez 1998-2009

typical satellite

V5 Completely new web application 1020 Class I and II 2014 September user interface, updated calculation TMY3s (default), 239 2014 engine (described here). Avail­ TMY2s, 360 Internaable at http://pvwatts.nrel.gov. tional, 10 km CPR/Perez Also available as a web service on 1998-2009 typical satellite http://developer.nrel.gov

PVsyst is another option for detailed PV performance modeling, and is a commercial software product [5].

#### 2

#### Overview of Changes in Version 5

PVWatts version 5 is a comprehensive update of both default values and algorithms. The changes are designed to more accurately model typical systems while keeping the number of inputs to a minimum, and to provide a way to diﬀerentiate between common technology options without posing an undue technical burden upon the user.

For reference, previous versions of the PVWatts calculations are described in [1]. The key changes in PVWatts V5 are:

- 1. Option to select “Standard”, “Premium”, or “Thin ﬁlm” module type.
- 2. Option to specify a DC-to-AC nameplate sizing ratio.
- 3. Module model no longer includes a quadratic correction at low light levels.


- 4. Total system losses are speciﬁed as a percentage, with a default value of 14 %. This replaces the former DC-to-AC derate factor in PVWatts V1.
- 5. Inverter eﬃciency curve is derived from statistical analysis of data on inverters manufactured since 2010. The nominal inverter eﬃciency can be entered by the user.
- 6. One-axis tracking systems either estimate linear beam+diﬀuse self-shading losses based on row spacing, or use backtracking.
- 7. Albedo is ﬁxed at 0.2 unless explicitly speciﬁed at each hour in a TMY3, EPW, or SAM/CSV weather ﬁle.


#### 3

#### Model Inputs

PVWatts requires the minimal set of PV system speciﬁcations as listed in Table 2. Other performance parameters such as module temperature coeﬃcients are hidden from the user.

Table 2. Input Parameters

Field Units Default Value System size kW (DC) 4 Module type Standard, Premium, Thin ﬁlm Standard System losses % 14 Array type Fixed open rack, Fixed roof mount, 1-Axis, Fixed open rack

Backtracked 1-Axis, 2-Axis Tilt angle degrees Site Latitude Azimuth angle degrees 180◦ in northern hemi­

sphere, 0◦ in southern hemisphere

Advanced inputs DC/AC ratio ratio 1.1 Inverter eﬃciency % 96 GCR (1 Axis only) fraction 0.4

The new module type input is designed to help diﬀerentiate between diﬀerent technology options. The “standard” option represents typical poly- or mono-crystalline silicon modules, with eﬃciencies in the range of 14-17 %. The “premium” option is appropriate for modeling high eﬃciency (∼18-20 %) monocrystalline silicon modules that have anti-reﬂective coatings and lower temperature coeﬃcients. The thin ﬁlm option assumes a low eﬃciency (∼11 %), and a signiﬁcantly lower temperature coeﬃcient which is representative of most installed thin ﬁlm modules as of 2013. It is important to note that less common thin ﬁlm module technologies may have quite diﬀerent temperature coeﬃcients than the default. The model assumptions for each model type are listed in Table 3. It is up to the user to select the most appropriate option for the type of module being considered based on information on the module data sheet. The “standard” option is appropriate for typical preliminary analyses and is most similar to PVWatts V1.

The new advanced inputs allow the user to specify a DC-to-AC sizing ratio and ground coverage ratio, which was not possible in older versions of PVWatts. PVWatts V1 assumed that the DC nameplate capacity of the system was equal to the AC nameplate capacity. In modern

Table 3. Assumptions for diﬀerent module types

Module type Eﬃciency Cover type Temperature coeﬃcient Standard ∼15 % Glass -0.47 %/◦C Premium ∼19 % Anti-reﬂective -0.35 %/◦C Thin ﬁlm ∼10 % Glass -0.20 %/◦C

systems, the photovoltaic array is often sized so that its DC rating is higher than the inverter’s AC rating. Depending on location, this may be desirable to capture more energy during the beginning and end of the day, despite possibly clipping output at peak sun hours. The default value of the new DC-to-AC ratio input is 1.1. For a 4 kW DC system, this would result in a 3.63 kW AC inverter rating.

The ground coverage ratio (GCR) only applies to one axis tracking systems. It is a measure of the total module area relative to the roof or ground space occupied by the array. A GCR of 0.5 means that for a horizontal roof or ground surface, half of the total area is covered by modules when the tracker is rotated such that they are horizontal. A lower GCR means wider spacing between rows, and a higher one means that rows are spaced closer together. A GCR of 1 indicates no space between adjacent rows, and a GCR of 0 means essentially inﬁnite spacing between rows. Typical one axis tracker systems have GCRs in the range of 0.3 to 0.6, and the default value in PVWatts is 0.4. Previous versions of PVWatts eﬀectively assumed a GCR of zero, which is impossible to achieve in practice.

#### 4

#### Solar Resource

PVWatts requires hourly data for one year for two components of solar irradiance (beam and diﬀuse), ambient dry bulb temperature, and wind speed at 10 m above the ground. Each hour be timestamped with the year, month, day, and hour corresponding to the data line so that the sun position can be accurately calculated.

No adjustments are made for leap years or daylight savings time: hence, “hourly data” in this context implies 8,760 data points for one year. The required data are listed in Tables 4 and 5.

Table 4. Header Information

Field Units Latitude degrees Longitude degrees Time zone hours oﬀset from Greenwich Mean Time Site elevation meters above sea level

PVWatts can read solar resource data ﬁles from diﬀerent sources and in diﬀerent formats, including the National Solar Radiation Database (NSRDB) 1961-1990 data (TMY2) and 1991-2010 update (TMY3), and EnergyPlus weather ﬁles. It also reads ﬁles in the SAM CSV format [4], which is a generic format suitable for custom solar resource data sets. The PVWatts web application interacts with three online databases to access solar resource data, but does not allow users to specify their own weather data.

Table 5. Hourly Input Data Fields

Field Units/Values Year 1950-2050 Month 1-12 Day 1-31 Hour 0-23 Direct normal irradiance (DNI) W/m2 Diﬀuse horizontal irradiance (DHI) W/m2 Ambient dry bulb temperature Celsius Wind speed at 10 m m/s Albedo (optional, typically in TMY3 ﬁles) [0..1]

|Change from PVWatts V1 In PVWatts V1, the albedo was changed to 0.6 for hours with a positive snow depth when using a TMY2 ﬁle. This increased system output, assuming the modules were cleaned regularly of any snow cover. Now, PVWatts assumes an albedo of 0.2 for all hours of the year for TMY2 ﬁles, and uses the hourly value provided in TMY3 ﬁles.|
|---|


#### 5 Sun Position

At each hour, PVWatts calculates the sun position using the algorithm described in [6]. The sun position is calculated at the midpoint of the hour: for example, from 2 p.m. to 3 p.m., the sun position is calculated at 2:30 p.m. to determine the solar zenith and azimuth angles. This is the case for normal daytime hours during which the sun is above the horizon for the whole hour.

For the sunrise hour, the midpoint between the sunrise time and the end of the timestep is used for the sun position calculation. Similarly, the midpoint between the beginning of the timestep and sunset time is used for the sunset hour.

#### 6 Tracking

PVWatts performs angle of incidence (AOI) (α) calculations for ﬁxed, one-axis, or two-axis tracking systems.

Fixed systems implement standard geometrical calculations for the angle of incidence given surface tilt β, surface azimuth γ, solar azimuth γsun, and solar zenith θsun angles, as listed in Eqn. 1.

αfixed = cos −1 [sin(θsun) cos(γ − γsun) sin(β) + cos(θsun) cos(β)] (1)

For one axis trackers, the algorithm documented in [10] is used. It assumes ideal tracking and does not account for any shading. The one-axis tracking algorithm assumes a hard-coded rotation limit of ± 45 degrees from the horizontal. PVWatts uses a separate algorithm to calculate the fraction of each row that is shaded by adjacent rows based on the ground coverage ratio (GCR), and reduces the beam and diﬀuse irradiance incident on each row accordingly. When the backtracking option is enabled, PVWatts uses the SAM backtracking algorithm to avoid self-shading of adjacent rows. For details on these algorithms, consult [25].

|Change from PVWatts V1 In PVWatts V1, one axis tracking assumed no selfshading or backtracking. This is an unrealistic assumption for most installed systems, as tracking rows cannot be spaced inﬁnitely apart. Consequently, the production estimates for one axis tracked systems will be reduced relative to PVWatts V1.|
|---|


For two axis tracking systems, the PV surface tilt and azimuth are set equal to the sun zenith angle and the sun azimuth angle, respectively, and the incidence angle is zero. The two axis tracking algorithm assumes no shading.

#### 7 Plane-of-Array Irradiance

The plane-of-array (POA) beam, sky diﬀuse, and ground-reﬂected diﬀuse irradiance components are calculated using the Perez 1990 algorithm [7]. The POA beam component Ib is simply the beam normal input multiplied by the cosine of the angle of incidence. The isotropic, circumsolar, and horizon brightening diﬀuse terms are calculated from the beam and diﬀuse input given two empirical functions F1 and F2 as deﬁned and are summed to yield the total sky diﬀuse on the surface Id,sky. A slight modiﬁcation from the standard Perez model treats the diﬀuse irradiance as isotropic for zenith angles between 87.5 and 90 degrees. The ground reﬂected irradiance Id,ground is treated as isotropic diﬀuse with a view factor calculated from the ground with respect to the tilted surface. The total POA incident on the module cover is the sum of the three components (Eqn. 2).

Ipoa = Ib + Id,sky + Id,ground (2)

The albedo, or ground reﬂectance, is by default ﬁxed at 0.2. When using TMY3 data as input, and valid data is found in the albedo column, the hourly albedo from the data ﬁle is used.

#### 8 Module Cover

Given the total POA irradiance incident on the module cover, PVWatts applies an AOI correction to adjust the direct beam irradiance to account for reﬂection losses. The correction uses a modiﬁed version of the physical model of transmittance through a module cover used in [19].

PVWatts V5 gives users the option of “Standard”, “Premium”, or “Thin ﬁlm” modules. For standard and thin ﬁlm modules, PVWatts uses a single slab, calculating the transmittance through glass with index of refraction of 1.526. This follows the treatment in [19], with the simpliﬁcation of removing the absorptance term which is determined (see below) to have a negligible eﬀect.

For the premium module option, a two slab approach is used to model both the glass and the thin anti-reﬂective (AR) coating that is designed to improve the angular response. The two slab model involves predicting the transmittance of irradiance through two materials. The model applies the physical representation for unpolarized radiation described in [19] twice: once for the anti-reﬂective (AR) coating, and subsequently for the glass cover.

First, the angle of refraction θ2 into the AR coating is calculated with Snell’s law given angle of incidence θ1:

nair θ2 = arcsin sin(θ1) (3) nAR

θ1

Air (n=1)

θ2

AR (n=1.3)

Glass (n=1.5)

θ3

Figure 1. Diagram of two slab model

Next, the transmittance through the AR coating is calculated from Fresnel’s equation for non-reﬂected unpolarized radiation, which takes the average of parallel and perpendicular components.

sin(θ2 − θ1)2 tan(θ2 − θ1)2 τAR = 1 − 0.5 + (4) sin(θ2 + θ1)2 tan(θ2 + θ1)2

The angle of refraction into the glass cover θ3 is again determined from Snell’s law.

nAR θ3 = arcsin sin(θ2) (5) nglass

The transmittance through the glass is calculated similarly given θ2 and θ3.

sin(θ3 − θ2)2 tan(θ3 − θ2)2 τglass = 1 − 0.5 + (6) sin(θ3 + θ2)2 tan(θ3 + θ2)2

Finally, the eﬀective transmittance through the AR coated module cover is given by:

τcover = τARτglass (7)

Desoto [19] suggests using Bouguer’s law to estimate the absorption, but for typical dimensions (∼2 mm) and extinction coeﬃcients (K ≈ 4) in this application, the absorption is predicted to be less than 0.1 % and is thus ignored.

Given nair = 1 and nglass = 1.526, the angular response for two diﬀerent indices of refraction for the AR coating is shown in Fig. 2. The model suggests that an AR coating yields an improvement in transmittance of about 3 % relative to standard glass at normal incidence, which is commensurate with claims made by industry (Honeywell SOLARC [20], DSM Khepricoat [21]).

Normalizing the response curve to normal incidence shows that the model predicts an improvement in light capture at high incidence angles for AR glass, which agrees with data from manufacturers of AR coated modules (Fig. 3).

|Change from PVWatts V1 In PVWatts V1, the angular response correction was only applied for incidence angles greater than 50 degrees. The new approach uses a physical model instead, which makes it possible to model typical diﬀerences between standard glass and anti-reﬂective glass.|
|---|


Angular response

- 0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8

0.9

- 1


Covertransmittance

|Standard Glass<br><br>Physical AR (n=1.3)<br><br>Physical AR (n=1.4)<br><br><br>|
|---|


0 10 20 30 40 50 60 70 80 90 Angle of incidence (deg)

###### Figure 2. Two slab model angular response compared with single slab model

Normalized angular response

- 0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8

0.9

- 1


Covertransmittance

|standard glass<br><br>AR glass (nar=1.3)<br><br>|
|---|


0 10 20 30 40 50 60 70 80 90 Angle of incidence (deg)

###### Figure 3. Two slab model angular response compared with single slab model - normalized

The AR glass option will predict slightly higher output compared with the standard option due to the improved angular response. The normal incidence transmittance of the module cover is assumed to be captured in the nameplate rating of the system. The additional energy output due to the better angular response for AR glass is slight: for a ﬁxed south-facing system in Texas, the anti-reﬂective coating yielded about ∼0.5 % more energy on an annual basis. This will vary depending on location and system parameters.

#### 9

Thermal Model

PVWatts implements a thermal model to calculate the operating cell temperature Tcell using a ﬁrst-principles heat transfer energy balance model developed by Fuentes [15]. The Fuentes model includes eﬀects of the thermal capacitance of the module and performs a numerical integration between timesteps to account for the thermal lag transient behavior. The thermal model uses the total incident POA irradiance, wind speed, and dry bulb temperature to calculate the operating cell temperature. PVWatts assumes a height of 5 m above the ground when correcting the wind speed in the weather data, and that the installed nominal operating cell temperature (INOCT) of the module is 45 ◦C.

|Change from PVWatts V1 In PVWatts V5, ﬁxed systems may be mounted on an open rack or a roof mount. The selection changes the assumed INOCT based on the reduced air ﬂow and thus higher operating temperature of a roof mount system.|
|---|


The Fuentes paper discusses translation of the nominal operating cell temperature (NOCT) measured at standard conditions (800 W/m2, 20◦C ambient) to INOCT based on mounting conﬁguration. For a roof mount system, air ﬂow around the modules more restricted than on an open rack, and the installed nominal operating temperature will be higher. The estimate is for INOCT to be roughly 49 ◦C for 4 inch standoﬀs. For ﬁxed open rack and tracking systems, the original PVWatts V1 assumption of 45 ◦C INOCT is retained.

#### 10 Module Model

The PVWatts module computes the DC power from the array with a speciﬁed nameplate DC rating of Pdc0 given a computed cell temperature Tcell and transmitted POA irradiance Itr. The array eﬃciency is assumed to decrease at a linear rate as a function of temperature rise, governed by temperature coeﬃcient γ. The reference cell temperature Tref is 25◦C, and reference irradiance is 1000 W/m2 .

Itr Pdc = Pdc0(1 + γ(Tcell − Tref )) (8) 1000

|Change from PVWatts V1 In PVWatts V1, a quadratic correction was used to reduce the output for irradiance less than 125 W/m2 . In comparison with operating data from many systems, this behavior was not observed in modern systems, and thus the correction was removed.|
|---|


The temperature coeﬃcent depends on the module type selected. The values used were determined from a statistical analysis of over 11000 modules in the CEC module database, and are listed in Table 3.

|Change from PVWatts V1 PVWatts V1 used a ﬁxed temperature coeﬃcient of<br><br>-0.5%/◦C . The new values indicate improved performance of newer modules.|
|---|


#### 11 System Losses

Losses in the system that are not explicitly modeled are provided by the user as a percentage of DC energy. Losses represented by this number include the impacts of soiling, shading, snow cover, mismatch, wiring, connections, light induced degradation, nameplate rating, system age, and operational availability. The default values are listed in Table 6, alongside the related default derates used in PVWatts V1. In V5, all wiring losses are combined into one loss category, and the inverter is explicitly modeled. Consult [12] for more information on loss assumptions.

Table 6. System Losses

Loss mechanism Default value Related V1 Derate Soiling 2 % 0.95 Shading 3 % 1.0 Snow 0 % 1.0 Mismatch 2 % 0.98 Wiring 2 % 0.98 AC Wiring – 0.99 Connections 0.5 % 0.995 Light-induced degradation 1.5 % – Nameplate rating 1 % 0.95 Age 0 % 1.0 Availability 3 % 0.98 Inverter – 0.92 Total losses 14 % (via Eqn. 9) 0.77

It is important to note that the total loss is not the sum of the individual losses. The total loss is calculated by multiplying the reduction due to each loss Li (%) as shown in Eqn. 9. The default total system loss is calculated to be 14 %.

Li 100

Ltotal(%) = 100 1 − 1 −

i

(9)

The default assumption for shading losses represents blocking of the horizon due to faraway features such as large buildings, mountains, or other obstructions. Surveys of installed systems indicated that the average losses due to shading on systems described as “unshaded” was roughly 3 % [14]. For a system experiencing shading due to nearby trees or structures, this loss value should be increased appropriately by using external shading software to predict shading losses, or with a onsite survey.

Light-induced degradation (LID) is a phenomenon in which the power output of a module decreases when it is exposed to sunlight for the ﬁrst time. After this initial period, the module power stabilizes and subsequently follows typical long-term degradation over the lifetime of the installation (∼ 0.5 %/year). The default light-induced degradation (LID) loss of 1.5 % is a typical value based on measurements of losses in diﬀerent module types [13]. Some premium modules may experience lower LID losses due to their materials and construction, while others may experience LID losses greater than 1.5 %.

|Change from PVWatts V1 PVWatts V1 used a DC-to-AC derate factor with a default value of 0.77. The decision to switch to a system loss percentage input was made to bring PVWatts in line with common practice in the industry, and to make the inputs easier to understand for people not familiar with the concept of a derate factor. The inverter eﬃciency is not included in the system loss, and is a separate input parameter.|
|---|


To approximately convert PVWatts V5 system loss to a PVWatts V1 DC-to-AC derate factor:

- 1. Convert the system loss to a derate: 1 − 14/100 = 0.86.
- 2. Multiply this value by the nominal inverter eﬃciency: 0.86 × 0.96 = 0.825


This suggests that the default PVWatts V5 system loss represents roughly a 7 % increase in system performance relative to PVWatts V1 due solely to updated input assumptions. The impact of the revised inverter eﬃciency curve in version 5 (described in next section) places the realized performance gain relative to V1 closer to 8-9 % on an annual energy basis. This behavior is commensurate with hundreds of reports from PVWatts users, an expert survey solicitation, and calibration to numerous measured datasets that suggested that the old PVWatts derate was two conservative and underpredicted modern system performance by at least 8-9 % on average.

#### 12 Inverter Model

The inverter model in PVWatts V5 is based on an analysis of California Energy Commission (CEC) inverter performance data. Inverters newer than 2010 were included in the analysis. A “typical” inverter was selected from the dataset by ﬁrst calculating an average part-load eﬃciency curve, and then ﬁnding the actual inverter in the dataset whose actual eﬃciency curve was closest to the average. The eﬃciency data was then ﬁtted to a quadratic loss model as presented in [22]. The resulting performance curve is given in Eqn. 10, which scales the eﬃciency curve to the nominal rated eﬃciency speciﬁed by the user ηnom. The reference inverter eﬃciency ηref from the CEC data for the actual most typical inverter is 0.9637 (Pac0/Pdc0), and AC nameplate rating Pac0 is determined from the DC rating of the system and the DC-to-AC ratio. The default nominal eﬃciency ηnom is 0.96.

ηnom 0.0059 Pdc Pac0

η = −0.0162 · ζ − + 0.9858 where ζ = and Pdc0 = (10) ηref ζ Pdc0 ηnom

When the predicted AC output exceeds the nameplate rating, the output is clipped to the nameplate value. The inverter eﬃciency is shown in Fig. 4 for diﬀerent nominal eﬃciencies, along with the original version 1 curve.

⎧ ⎨ ηPdc : 0 < Pdc < Pdc0

Pac = Pac0 : Pdc ≥ Pdc0 (11) ⎩

0 : Pdc = 0

Inverter Part−Load Efficiency

- 0

0.1

0.2

0.3

0.4

0.5

0.6

0.7

0.8

0.9

- 1


Efficiency

|η=99% =98%<br><br>=96% (default)<br><br>=94% =92%<br><br>PVWatts V1<br><br>|
|---|


η η η η

0 0.2 0.4 0.6 0.8 1

Load fraction

Figure 4. Inverter part-load eﬃciency curve Table 7. Hourly Calculated Outputs

Field Units Incident POA irradiance W/m2 Transmitted POA irradiance W/m2 DC power W AC power W

#### 13 Model Outputs

PVWatts reports several hourly outputs based on the system speciﬁcations and hourly irradiance, temperature, and wind speed data. They are summarized in Table 7.

In addition, the average incident POA irradiance per day in each month is reported to the user. For each month m, the average POA in (kW/m2/day) is given by Eqn. 12.

0.001 · m P OAh P OAm = (12) number of days in month m

The hourly outputs DC and AC power are also aggregated into monthly and annual energy totals that are reported to the user.

#### 14 Comparison with Version 1 Results

Energy predictions of PVWatts V5 were compared to PVWatts V1 for several TMY2 locations. Several scenarios were considered:

- 1. Fixed: Fixed 20 degree tilt, south facing, standard module
- 2. Fixed+Premium: Fixed 20 degree tilt, south facing, premium module in PVWatts V5
- 3. 1 Axis: Self-shaded one axis tracking, GCR 0.4, standard module
- 4. Backtracking: Backtracked one axis tracking, GCR 0.4, standard module
- 5. 2 Axis: Two axis tracking, standard module


The number for each scenario reported in Table 8 is the percent diﬀerence between PVWatts V5 and V1 annual AC energy production estimates. The results show that PVWatts V5 predicts on average 8 % percent more annual energy across all system conﬁgurations and locations. The one axis tracking cases show a lower increase - this is because PVWatts V1 overpredicts one axis tracking by assuming no self shading of rows. The greater relative improvement for ﬁxed systems is due to the fact that ﬁxed arrays operate more frequently at part-load since they do not track the sun, and so the eﬀect of the improved part-load inverter eﬃciency is more pronounced.

#### 15 Comparison with Measured Data

In this section, PVWatts predictions are shown for several systems. The nine systems considered are detailed in [23], and consist of 8 ﬁxed tilt systems and one 1-axis tracked system. PVWatts V1 underpredicts system performance by 11.9 % when comparing annual AC energy, while PVWatts V5 is low by only 1.8 %. All of the systems considered were unshaded, and the periods during which the system was unavailable were removed from the comparison. Consequently, the loss mechanisms for shading and availability were set to zero for both models. Systems with nonstandard module types were conﬁgured appropriately in PVWatts V5: system 2 (premium), system 7 (thin-ﬁlm), and system 9 (thin-ﬁlm).

In Figure 6, PVWatts V1 hourly results are shown for a ﬁxed crystalline silicon system in Colorado. The data does not support the quadratic behavior at low power levels predicted by V1. PVWatts V5 does not include the module performance adjustment below 125 W/m2, and thus matches the measured system data better. The PVWatts V1 low irradiance assumptions are not supported by any of the modern systems considered. In addition, the updated inverter performance curve in V5 tracks the measured system output more closely at high power outputs.

#### 16 Summary

A comprehensive update to the popular PVWatts photovoltaic performance model was presented. The improved model formulation and updated default assumptions in V5 largely correct the underprediction of V1 relative to actual system performance. The updated PVWatts will be deployed to the NREL PVWatts Online Calculator in the fall of 2014, available at http://pvwatts.nrel.gov.

Measured vs PVWatts V1 and V5 for Several Systems

10

PercentagedifferenceinannualACenergy

|PVWatts V1 PVWatts V5<br><br>| |
|---|
<br><br>| |
|---|
|
|---|


5

0

V5 Avg: −1.8 %

−5

−10

V1 Avg: −11.9 %

−15

−20

1:Fixed(c−Si)2:Fixed(c−Si)3:Fixed(c−Si)4:Fixed(c−Si)5:Fixed(c−Si)6:1Axis(c−Si)7:Fixed(CdTe)8:1Axis(c−Si)9:Fixed(CdTe)

###### Figure 5. Comparision of PVWatts V1 and V5 AC energy prediction vs measured

Hourly Energy Production

400

350

300

Modeled−ACenergy(kWh)

250

200

150

100

50

|PVWatts V1 PVWatts V5 Measured<br><br>|
|---|


0

−50

0 50 100 150 200 250 300 350 400

Measured − AC energy (kWh)

###### Figure 6. Hourly PVWatts V1 and V5 predictions vs measured

#### References

- [1] Dobos, A.; PVWatts Version 1 Technical Reference. . NREL/TP-6A20-60272. 2013.
- [2] Marion, W.; Urban, K. (2012). User’s Manual for TMY2. Accessed September 3, 2013: http://rredc.nrel.gov/solar/pubs/tmy2/.
- [3] Wilcox, S.; Marion, W. (2008). User’s Manual for TMY3 Data Sets. NREL/TP-581-43156. Golden, CO: National Renewable Energy Laboratory.
- [4] NREL. System Advisor Model (SAM). http://sam.nrel.gov. 2014.
- [5] PVsyst SA. PVsyst Photovoltaic Software Version 6.1. http://www.pvsyst.com. 2014.
- [6] Michalsky, J. (1988). “The Astronomical Almanac’s Algorithm for Approximate Solar Position (1950-2050).” Solar Energy (40).
- [7] Perez, R.; Ineichen, P.; Seals, R.; Michalsky, J.; Stewart, R. (1990). “Modeling Daylight Availability and Irradiance Components for Direct and Global Irradiance.” Solar Energy (44:5), pp. 271-289.
- [8] Marion, W.; Anderberg, M. (2000). PVWATTS - An Online Performance Calculator for Grid-Connected PV Systems. Proceedings of the ASES Solar Conference, June 15-21, 2000, Madison, Wisconsin.
- [9] Marion, W.; Anderberg, M.; George, R.; Gray-Hann, P.; Heimiller, D.; (2001) PVWATTS Version 2 - Enhanced Spatial Resolution for Calculating Grid-Connected PV Performance. CP-560-30941. Golden CO: National Renewable Energy Laboratory.
- [10] Marion, W.; Dobos, A. P. (2013). Rotation Angle for the Optimum Tracking of One-Axis Trackers. TP-6A20-58891. Golden, CO: National Renewable Energy Laboratory.
- [11] Marion, W. (2010). Overview of the PV Module Model in PVWatts. Presentation at the Sandia National Laboratories PV Performance Modeling Workshop, September 22, 2010, Albuquerque, New Mexico.
- [12] Marion, W.; Adelstein, J.; Boyle, K.; Hayden, H.; Hammond, B.; Fletcher, T.; Canada, B.; Narang, D.; Shugar, D.; Wenger, H.; Kimber, A.; Mitchell, L.; Rich, G.; Townsend, T. (2005). Performance Parameters for Grid-Connected PV Systems. Proc. of 31st IEEE Photovoltaics Specialists Conference, January 2005, Lake Buena Vista, Florida.
- [13] Pingel, S., Koshnicharov, D., Frank, O., Geipel, T., Zemen, Y., Striner, B., Berghold, J. Initial degradation of industrial silicon solar cells in solar panels. 25th EU PVSEC, 2010.
- [14] Deline, C.; Meydbray, J.; Donovan, M.; Forrest, J.; Photovoltaic Shading Testbed for Module-level Power Electronics. NREL Technical Report NREL/TP-5200-54876, May 2012. http://www.nrel.gov/docs/fy12osti/54876.pdf
- [15] Fuentes, M. K. (1987). A Simpliﬁed Thermal Model for Flat-Plate Photovoltaic Arrays. SAND85-0330. Albuquerque, NM: Sandia National Laboratories. Accessed September 3, 2013: http://prod.sandia.gov/techlib/access-control.cgi/1985/850330.pdf.
- [16] California Energy Commission. (2013). “CEC PV Calculator Version 4.0.” Accessed September 3, 2013: http://gosolarcalifornia.org/tools/nshpcalculator/index.php.


- [17] Menicucci, D. F.; Fernandez, J. P. (1988). User’s Manual for PVFORM: A Photovoltaic System Simulation Program For Stand-Alone and Grid-Interactive Applications. SAND85-0376. Albuquerque, NM: Sandia National Laboratories. Accessed September 3, 2013: http://prod.sandia.gov/techlib/access-control.cgi/1985/850376.pdf.
- [18] Menicucci, D. F. (1986). Photovoltaic Array Performance Simulation Models. Solar Cells

(18).

- [19] DeSoto, W.; Klein, S.; Beckman, W.; Improvement and Validation of a Model for Photovoltaic Array Performance. Solar Energy, vol.80, pp.78-88, 2006.
- [20] Honeywell SOLARC. http://www.honeywell-pmt.com/sm/em/common/documents/SOLARC antireﬂective coating.pdf.
- [21] DSM Khepricoat. https://www.dsm.com/content/dam/dsm/cworld/en US/documents/khepricoatboosting-module-performance-with-a-durable-ar-coating.pdf
- [22] Dreisse, A.; Jain, P.; Harrison, S.; Beyond the Curves: Modeling the Electrical Eﬃciency of Photovoltaic Inverters. Proc. IEEE Photovoltaic Specialists Conf., 2008.
- [23] Freeman, J.; Whitmore, J.; Kaﬃne, L.; Blair, N.; Dobos, A.; System Advisor Model: Flat Plat Photovolatic Performance Modeling Validation Report. NREL/TP-6A20-60204, 2013.
- [24] Freeman, J.; Whitmore, J.; Blair, N.; Dobos, A.; Validation of Multiple Tools for Flat Plate Photovoltaic Modeling Against Measured Data. NREL/TP-6A20-61497, 2014.
- [25] Gilman, P.; SAM Photovoltaic Model Technical Reference. NREL/TP-6A20-xxxxx, forthcoming, 2014.


Table 8. Comparison with PVWatts V1 for selected TMY2 locations Location Fixed Fixed+Premium 1 Axis Backtracking 2 Axis

- AK Anchorage 14.7 % 14.3 % 6.8 % 8.0 % 9.6 %
- AL Huntsville 9.7 % 11.2 % 4.9 % 5.9 % 8.5 % AR Little Rock 9.8 % 11.5 % 4.7 % 5.6 % 8.5 % AZ Phoenix 8.8 % 12.1 % 3.7 % 3.9 % 8.0 % CA Sacramento 9.2 % 11.2 % 4.0 % 4.5 % 8.2 % CO Boulder 8.9 % 10.2 % 3.3 % 3.9 % 7.3 % CT Hartford 10.2 % 10.7 % 5.0 % 6.3 % 8.0 % DE Wilmington 9.9 % 10.8 % 4.9 % 5.9 % 8.3 % FL Miami 9.4 % 11.5 % 4.7 % 5.7 % 8.3 % GA Atlanta 9.5 % 11.0 % 4.6 % 5.4 % 8.4 % HI Honolulu 8.7 % 10.9 % 3.0 % 3.4 % 7.8 % IA Des Moines 9.6 % 10.3 % 4.2 % 4.9 % 8.0 % ID Boise 9.4 % 10.6 % 3.2 % 3.6 % 8.1 % IL Chicago 10.1 % 10.7 % 4.7 % 5.7 % 8.4 % IN Indianapolis 10.0 % 10.8 % 4.9 % 6.0 % 8.5 % KS Wichita 9.3 % 10.4 % 4.0 % 4.6 % 8.0 % KY Lexington 10.1 % 11.0 % 5.0 % 6.0 % 8.7 % LA New Orleans 9.9 % 11.8 % 5.3 % 6.4 % 8.6 % MA Boston 9.8 % 10.2 % 4.7 % 5.7 % 8.0 % MD Baltimore 10.0 % 10.9 % 4.9 % 5.9 % 8.4 % ME Portland 9.6 % 9.8 % 3.9 % 4.8 % 6.9 % MI Detroit 10.5 % 10.9 % 4.9 % 6.1 % 8.2 % MN Minneapolis 9.5 % 9.8 % 3.7 % 4.5 % 6.9 % MO Springﬁeld 9.6 % 10.8 % 4.4 % 5.1 % 8.3 % MS Jackson 9.8 % 11.6 % 5.2 % 6.2 % 8.5 % MT Great Falls 9.7 % 10.1 % 3.5 % 4.2 % 7.3 % NC Charlotte 9.7 % 11.2 % 4.9 % 5.8 % 8.5 %


- ND Fargo 9.6 % 9.6 % 3.3 % 4.1 % 6.6 %
- NE Omaha 9.5 % 10.4 % 4.2 % 5.0 % 7.5 % NH Concord 9.8 % 10.3 % 4.3 % 5.2 % 7.6 % NJ Newark 10.2 % 10.8 % 5.3 % 6.4 % 8.6 % NM Albuquerque 8.5 % 10.3 % 3.6 % 4.0 % 7.6 % NV Las Vegas 8.5 % 11.2 % 3.0 % 3.1 % 7.8 % NY Albany 10.2 % 10.6 % 4.4 % 5.4 % 8.0 % OH Cleveland 10.8 % 11.4 % 5.3 % 6.5 % 8.6 % OK Tulsa 9.5 % 10.8 % 4.2 % 4.9 % 8.4 % OR Portland 11.6 % 12.6 % 5.6 % 6.6 % 9.9 % PA Harrisburg 10.0 % 10.9 % 5.0 % 6.0 % 8.6 % RI Providence 9.8 % 10.2 % 4.8 % 5.8 % 8.1 % SC Charleston 9.5 % 11.1 % 4.7 % 5.5 % 8.4 % SD Sioux Falls 9.6 % 10.1 % 3.8 % 4.5 % 7.1 % TN Chattanooga 10.1 % 11.7 % 5.4 % 6.4 % 9.0 % TX Abilene 8.9 % 10.6 % 3.6 % 4.1 % 7.9 % UT Salt Lake City 9.4 % 10.9 % 3.6 % 4.1 % 7.8 % VA Richmond 9.8 % 10.9 % 4.8 % 5.7 % 8.4 % VT Burlington 10.1 % 10.3 % 4.1 % 5.1 % 7.4 % WA Yakima 9.8 % 11.2 % 3.3 % 3.7 % 8.1 % WI Madison 9.9 % 10.2 % 4.6 % 5.7 % 7.8 %


WV Elkins 10.7 % 11.3 17 % 5.9 % 7.4 % 9.0 % WY Cheyenne 8.8 % 9.2 % 2.9 % 3.4 % 7.2 %

Average 9.8 % 10.9 % 4.4 % 5.3 % 8.1 %

