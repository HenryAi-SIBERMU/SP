![image 1](<nrel_spa_technical_report_34302_images/imageFile1.png>)

Revised January 2008 • NREL/TP-560-34302

# Solar Position Algorithm for Solar Radiation Applications

![image 2](<nrel_spa_technical_report_34302_images/imageFile2.png>)

Ibrahim Reda and Afshin Andreas

![image 3](<nrel_spa_technical_report_34302_images/imageFile3.png>)

![image 4](<nrel_spa_technical_report_34302_images/imageFile4.png>)

Revised January 2008 • NREL/TP-560-34302

# Solar Position Algorithm for Solar Radiation Applications

![image 5](<nrel_spa_technical_report_34302_images/imageFile5.png>)

### Ibrahim Reda and Afshin Andreas

Prepared under Task No. WU1D5600

![image 6](<nrel_spa_technical_report_34302_images/imageFile6.png>)

![image 7](<nrel_spa_technical_report_34302_images/imageFile7.png>)

![image 8](<nrel_spa_technical_report_34302_images/imageFile8.png>)

###### Acknowledgment

We thank Bev Kay for all her support by manually typing all the data tables in the report into text files, which made it easy and timely to transport to the report text and all of our software code. We also thank Daryl Myers for all his technical expertise in solar radiation applications.

###### NOTICE

This report was prepared as an account of work sponsored by an agency of the United States government. Neither the United States government nor any agency thereof, nor any of their employees, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States government or any agency thereof. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States government or any agency thereof.

Available electronically at http://www.osti.gov/bridge Available for a processing fee to U.S. Department of Energy and its contractors, in paper, from:

U.S. Department of Energy Office of Scientific and Technical Information P.O. Box 62 Oak Ridge, TN 37831-0062 phone: 865.576.8401 fax: 865.576.5728 email: reports@adonis.osti.gov

Available for sale to the public, in paper, from: U.S. Department of Commerce National Technical Information Service 5285 Port Royal Road Springfield, VA 22161 phone: 800.553.6847 fax: 703.605.6900 email: orders@ntis.fedworld.gov online ordering: http://www.ntis.gov/ordering.htm

Printed on paper containing at least 50% wastepaper, including 20% postconsumer waste

###### Table of Contents

Abstract ............................................................................................................................................v Introduction ......................................................................................................................................1 Time Scale .......................................................................................................................................2 Procedure .........................................................................................................................................3 SPA Evaluation and Conclusion ....................................................................................................12 List of Figures

- Figure 1. Uncertainty of cosine the solar zenith angle resulting from 0.01° and 0.0003° uncertainty in the angle calculation. ..................................................................................13
- Figure 2. Difference between the Almanac and SPA for the ecliptic longitude & latitude, and the apparent right ascension & declination on the second day of each month at 0-TT for the years 1994, 1995, 1996, and 2004 ...............................................................................14
- Figure 3. Difference between the Almanac and SPA for the solar zenith and azimuth angles on the second day of each month at 0-TT for the years 1994, 1995, 1996, and 2004. ...........15


References ......................................................................................................................................16 Appendix Equation of Time ........................................................................................................................ A-1 Sunrise, Sun Transit, and Sunset ................................................................................................ A-1 Calculation of Calendar Date from Julian Day ........................................................................... A-6 Example .................................................................................................................................... A-15 C source code for SPA .............................................................................................................. A-17

iii

###### List of Appendix Figures

Figure A2.1. Difference between the Almanac and SPA for the Ephemeris Transit on the second day of each month at 0-TT for the years 1994, 1995, 1996, and 2004. . . . . . . . . A-5

###### List of Appendix Tables

- Table A4.1. Examples for Testing any Program to Calculate the Julian Day . . . . . . . . . . . . . A-7
- Table A4.2. Earth Periodic Terms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A-7
- Table A4.3. Periodic Terms for the Nutation in Longitude and Obliquity . . . . . . . . . . . . . . A-13 Table A5.1. Results for Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . A-15


iv

###### Abstract

There have been many published articles describing solar position algorithms for solar radiation applications. The best uncertainty achieved in most of these articles is greater than ±0.01/ in calculating the solar zenith and azimuth angles. For some, the algorithm is valid for a limited number of years varying from 15 years to a hundred years. This report is a step by step procedure for implementing an algorithm to calculate the solar zenith and azimuth angles in the period from the year -2000 to 6000, with uncertainties of ±0.0003/. The algorithm is described by Jean Meeus [3]. This report is written in a step by step format to simplify the complicated steps described in the book, with a focus on the sun instead of the planets and stars in general. It also introduces some changes to accommodate for solar radiation applications. The changes include changing the direction of measuring azimuth angles to be measured from north and eastward instead of being measured from south and eastward, and the direction of measuring the observer’s geographical longitude to be measured as positive eastward from Greenwich meridian instead of negative. This report also includes the calculation of incidence angle for a surface that is tilted to any horizontal and vertical angle, as described by Iqbal [4].

v

###### 1. Introduction

With the continuous technological advancements in solar radiation applications, there will always be a demand for smaller uncertainty in calculating the solar position. Many methods to calculate the solar position have been published in the solar radiation literature, nevertheless, their uncertainties have been greater than ± 0.01/ in solar zenith and azimuth angle calculations, and some are only valid for a specific number of years[1]. For example, Michalsky’s calculations are limited to the period from 1950 to 2050 with uncertainty of greater than ± 0.01/ [2], and the calculations of Blanco-Muriel et al.’s are limited to the period from 1999 to 2015 with uncertainty greater than > ± 0.01/ [1].

An example emphasizing the importance of reducing the uncertainty of calculating the solar position to lower than ± 0.01/, is the calibration of pyranometers that measure the global solar irradiance. During the calibration, the responsivity of the pyranometer is calculated at zenith angles from 0/ to 90/ by dividing its output voltage by the reference global solar irradiance (G), which is a function of the cosine of the zenith angle (cos 2). Figure 1 shows the magnitude of errors that the 0.01/ uncertainty in 2 can contribute to the calculation of cos 2, and consequently G that is used to calculate the responsivity. Figure 1 shows that the uncertainty in cos 2 exponentially increases as 2 reaches 90/(e.g. at 2 equal to 87/, the uncertainty in cos 2 is 0.7%, which can result in an uncertainty of 0.35% in calculating G; because at such large zenith angles the normal incidence irradiance is approximately equal to half the value of G). From this arises the need to use a solar position algorithm with lower uncertainty for users that are interested in measuring the global solar irradiance with smaller uncertainties in the full zenith angle range from 0/ to 90/.

In this report we describe a procedure for a Solar Position Algorithm (SPA) to calculate the solar zenith and azimuth angle with uncertainties equal to ±0.0003/ in the period from the year -2000 to 6000. Figure 1 shows that the uncertainty of the reference global solar irradiance, resulting from ±0.0003/ in calculating the solar zenith angle in the range from 0/ to 90/ is negligible. The procedure is adopted from The Astronomical Algorithms [3], which is based on the Variations Sèculaires des Orbites Planètaires Theory (VSOP87) that was developed by P. Bretagnon in 1982 then modified in 1987 by Bretagnon and Francou [3]. In this report, we summarize the complex algorithm elements scattered throughout the book to calculate the solar position, and introduce some modification to the algorithm to accommodate solar radiation applications. For example, in The Astronomical Algorithms [3], the azimuth angle is measured westward from south, but for solar radiation applications, it is measured eastward from north. Also, the observer’s geographical longitude is considered positive west, or negative east from Greenwich, while for solar radiation applications, it is considered negative west, or positive east from Greenwich.

We start this report by: C Describing the time scales because of the importance of using the correct time in the SPA C Providing a step by step procedure to calculate the solar position and the solar incidence

angle for an arbitrary surface orientation using the methods described in An Introduction

to Solar Radiation [4]

C Evaluating the SPA against the Astronomical Almanac (AA) data for the years 1994,

1995, 1996, and 2004.

Because of the complexity of the algorithm we included some examples, in the Appendix, to give the users confidence in their step by step calculations. We also included in the Appendix an explanation of how to calculate the equation of time, sun transit (solar noon), sunrise, sunset, and how to change the Julian Day to a Calendar Date. We also included a C source code with header file, for all the calculations in this report (except for the Julian Day to Calendar Date conversion). The users can incorporate this module into their own code by including the header file, declaring the SPA structure, filling in the required input parameters into the structure, and then call the SPA calculation function. This function will calculate all the output values and fill in the SPA structure for the user.

The users should note that this report is used to calculate the solar position for solar radiation applications only, and that it is purely mathematical and not meant to teach astronomy or to describe the Earth rotation. For more description about the astronomical nomenclature that is used through out the report, the user is encouraged to review the definitions in the Astronomical Almanacs, or other astronomical reference.

- 2. Time Scale The following are the internationally recognized time scales:


C The Universal Time (UT), or Greenwich civil time, is based on the Earth’s rotation and counted from 0-hour at midnight; the unit is mean solar day [3]. UT is the time used to calculate the solar position in the described algorithm. It is sometimes referred to as UT1.

C The International Atomic Time (TAI) is the duration of the System International Second

(SI-second) and based on a large number of atomic clocks [5].

C The Coordinated Universal Time (UTC) is the bases of most radio time signals and the legal time systems. It is kept to within 0.9 seconds of UT1 (UT) by introducing one second steps to its value (leap second); to date the steps are always positive.

C The Terrestrial Dynamical or Terrestrial Time (TDT or TT) is the time scale of

ephemerides for observations from the Earth surface. The following equations describe the relationship between the above time scales (in seconds): TT = TAI + 32184. , (1) UT = TT − ∆ T , (2)

where )T is the difference between the Earth rotation time and the Terrestrial Time (TT). It is derived from observation only and reported yearly in the Astronomical Almanac [5].

![image 9](<nrel_spa_technical_report_34302_images/imageFile9.png>)

(3)

where )UT1 is a fraction of a second, positive or negative value, that is added to the UTC to adjust for the Earth irregular rotational rate. It is derived from observation, but predicted values are transmitted in code in some time signals, e.g. weekly by the U.S. Naval Observatory (USNO) [6].

###### 3. Procedure

###### 3.1. Calculate the Julian and Julian Ephemeris Day, Century, and Millennium:

The Julian date starts on January 1, in the year - 4712 at 12:00:00 UT. The Julian Day (JD) is calculated using UT and the Julian Ephemeris Day (JDE) is calculated using TT. In the following steps, note that there is a 10-day gap between the Julian and Gregorian calendar where the Julian calendar ends on October 4, 1582 (JD = 2299160), and after 10-days the Gregorian calendar starts on October 15, 1582.

- 3.1.1 Calculate the Julian Day (JD),


![image 10](<nrel_spa_technical_report_34302_images/imageFile10.png>)

(4) where,

- - INT is the Integer of the calculated terms (e.g. 8.7 = 8, 8.2 = 8, and -8.7 = 8..etc.).
- - Y is the year (e.g. 2001, 2002, ..etc.).
- - M is the month of the year (e.g. 1 for January, ..etc.). Note that if M > 2, then Y and M are not changed, but if M = 1 or 2, then Y = Y-1 and M = M + 12.
- - D is the day of the month with decimal time (e.g. for the second day of the month at 12:30:30 UT, D = 2.521180556).
- - B is equal to 0, for the Julian calendar {i.e. by using B = 0 in Equation 4, JD < 2299160}, and equal to (2 - A + INT (A/4)) for the Gregorian calendar {i.e. by using B = 0 in Equation 4, JD> 2299160}, where A = INT(Y/100).


For users who wish to use their local time instead of UT, change the time zone to a fraction of a day (by dividing it by 24), then subtract the result from JD. Note that the fraction is subtracted from JD calculated before the test for B<2299160 to maintain the Julian and Gregorian periods.

Table A4.1 shows examples to test any implemented program used to calculate the JD.

- 3.1.2. Calculate the Julian Ephemeris Day (JDE),

∆ T JDE = JD + . (5) 86400

- 3.1.3. Calculate the Julian century (JC) and the Julian Ephemeris Century (JCE) for the 2000 standard epoch,

JD − 2451545 JC = , (6) 36525

JDE − 2451545 JCE = . (7) 36525

- 3.1.4. Calculate the Julian Ephemeris Millennium (JME) for the 2000 standard epoch,


###### JCE JME = . (8) 10

###### 3.2. Calculate the Earth heliocentric longitude, latitude, and radius vector (L, B, and R):

“Heliocentric” means that the Earth position is calculated with respect to the center of the sun.

- 3.2.1. For each row of Table A4.2, calculate the term L0i (in radians), L0i = Ai *cos (Bi + Ci * JME) , (9)

where,

- - i is the ith row for the term L0 in Table A4.2.
- - Ai , Bi , and Ci are the values in the ith row and A, B, and C columns in Table A4.2, for the term L0 (in radians).


- 3.2.2. Calculate the term L0 (in radians),

n

L0= ∑ L0i , (10)

i = 0

where n is the number of rows for the term L0 in Table A4.2.

- 3.2.3. Calculate the terms L1, L2, L3, L4, and L5 by using Equations 9 and 10 and changing the 0 to 1, 2, 3, 4, and 5, and by using their corresponding values in


- columns A, B, and C in Table A4.2 (in radians).
- 3.2.4. Calculate the Earth heliocentric longitude, L (in radians),

L0 + L1* JME + L2* JME2 + L3* JME3 + L4* JME4 + L5* JME5 L = . (11) 108

- 3.2.5. Calculate L in degrees,

L(in R adians )*180 L (in Degrees) = , (12)

π

where B is approximately equal to 3.1415926535898.

- 3.2.6. Limit L to the range from 0/ to 360/. That can be accomplished by dividing L by 360 and recording the decimal fraction of the division as F. If L is positive, then the limited L = 360 * F. If L is negative, then the limited L = 360 - 360 * F.
- 3.2.7. Calculate the Earth heliocentric latitude, B (in degrees), by using Table A4.2 and steps 3.2.1 through 3.2.5 and by replacing all the Ls by Bs in all equations. Note that there are no B2 through B5, consequently, replace them by zero in steps 3.2.3 and 3.2.4.
- 3.2.8. Calculate the Earth radius vector, R (in Astronomical Units, AU), by repeating step 3.2.7 and by replacing all Ls by Rs in all equations. Note that there is no R5, consequently, replace it by zero in steps 3.2.3 and 3.2.4.


- 3.3. Calculate the geocentric longitude and latitude (1and $): “Geocentric” means that the sun position is calculated with respect to the Earth center.


- 3.3.1. Calculate the geocentric longitude, 1(in degrees), Θ = L + 180 . (13)
- 3.3.2. Limit 1to the range from 0/ to 360/ as described in step 3.2.6.
- 3.3.3. Calculate the geocentric latitude, $(in degrees), β= − B . (14)


##### 3.4. Calculate the nutation in longitude and obliquity ()Rand )g):

- 3.4.1. Calculate the mean elongation of the moon from the sun, X0 (in degrees),


###### X0 = 297.85036 + 445267111480. * JCE −

###### JCE3 0.0019142* JCE2 + . 189474

(15)

- 3.4.2. Calculate the mean anomaly of the sun (Earth), X1 (in degrees),


X1 = 357.52772 + 35999.050340* JCE −

3 (16) 2 JCE

0.0001603* JCE − . 300000

- 3.4.3. Calculate the mean anomaly of the moon, X2 (in degrees),

X2 = 134.96298 + 477198.867398* JCE +

(17)

2 JCE3 0.0086972* JCE + .

56250

- 3.4.4. Calculate the moon’s argument of latitude, X3 (in degrees),

X3 = 9327191. + 483202.017538* JCE −

JCE3 (18) 0.0036825* JCE2 + .

327270

- 3.4.5. Calculate the longitude of the ascending node of the moon’s mean orbit on the ecliptic, measured from the mean equinox of the date, X4 (in degrees),

X4 = 125.04452 − 1934.136261* JCE +

JCE3 (19) 0.0020708* JCE2 + .

450000

- 3.4.6. For each row in Table A4.3, calculate the terms )Ri and )gi (in 0.0001of arc seconds),


4

## ∆ψi = (ai + bi *JCE)*sin(∑ Xj *Yi,j) , (20)

j = 0

4

∆εi = (ci + di *JCE)*cos(∑ Xj *Yi,j) , (21)

j = 0

where,

- - ai , bi , ci , and di are the values listed in the ith row and columns a, b, c, and d in Table A4.3.
- - X j is the jth X calculated by using Equations 15 through 19.
- - Yi,j is the value listed in ith row and jth Y column in Table A4.3.


- 3.4.7. Calculate the nutation in longitude, )R(in degrees),

∑

n

∆ψ i ∆ψ = i= 0 , (22)

36000000

where n is the number of rows in Table A4.3 (n equals 63 rows in the table).

- 3.4.8. Calculate the nutation in obliquity, )g(in degrees),


n

∑

∆εi ∆ε = i= 0 . (23)

36000000

##### 3.5. Calculate the true obliquity of the ecliptic, g(in degrees):

- 3.5.1. Calculate the mean obliquity of the ecliptic, g0 (in arc seconds),


###### ε

= 84381448. − 4680 .93U − 155. U 2 + 1999 .25U 3 −

0

5138. U 4 − 249 .67U 5 − 39.05U 6 + 712. U 7 + (24) 27.87U 8 + 5.79U 9 + 2.45U10 ,

where U = JME/10.

- 3.5.2. Calculate the true obliquity of the ecliptic, g(in degrees),


ε0 ε= + ∆ε . (25)

3600

- 3.6. Calculate the aberration correction, )J(in degrees):

20.4898

∆τ= − . (26)

3600*R

- 3.7. Calculate the apparent sun longitude, 8(in degrees): λ= Θ + ∆ψ+ ∆τ . (27)
- 3.8. Calculate the apparent sidereal time at Greenwich at any given time, < (in degrees):

- 3.8.1. Calculate the mean sidereal time at Greenwich, <0 (in degrees),

ν0 = 280.46061837 + 360 .98564736629*(JD − 2451545) +

2 JC3 (28)

0.000387933* JC − . 38710000

- 3.8.2. Limit <0 to the range from 0/ to 360/ as described in step 3.2.6.
- 3.8.3. Calculate the apparent sidereal time at Greenwich, < (in degrees),


ν= ν0 + ∆ψ*cos ( ε) . (29)

- 3.9. Calculate the geocentric sun right ascension, "(in degrees):


- 3.9.1. Calculate the sun right ascension, " (in radians),


###### sinλ*cosε− tanβ*sinε α= Arctan2 ( ) , (30) cosλ

where Arctan2 is an arctangent function that is applied to the numerator and the denominator (instead of the actual division) to maintain the correct quadrant of the" where"is in the rage from -B to B.

- 3.9.2. Calculate "in degrees using Equation 12, then limit it to the range from 0/ to 360/ using the technique described in step 3.2.6.
- 3.10. Calculate the geocentric sun declination, *(in degrees): δ= Arcsin(sinβ*cosε+ cosβ*sinε*sinλ) , (31)


where*is positive or negative if the sun is north or south of the celestial equator, respectively. Then change * to degrees using Equation 12.

- 3.11. Calculate the observer local hour angle, H (in degrees): H = ν+σ−α , (32)

Where F is the observer geographical longitude, positive or negative for east or west of Greenwich, respectively.

Limit H to the range from 0/ to 360/ using step 3.2.6 and note that it is measured westward from south in this algorithm.

- 3.12. Calculate the topocentric sun right ascension "’ (in degrees):


“Topocentric” means that the sun position is calculated with respect to the observer local position at the Earth surface.

- 3.12.1. Calculate the equatorial horizontal parallax of the sun, >(in degrees),

8794.

ξ= , (33)

3600* R

where R is calculated in step 3.2.8.

- 3.12.2. Calculate the term u (in radians), u = A rctan (0.99664719*tanϕ) , (34)

wherenis the observer geographical latitude, positive or negative if north or south of the equator, respectively. Note that the 0.99664719 number equals (1 - f ), where f is the Earth’s flattening.

- 3.12.3. Calculate the term x,


E

6378140 * cosϕ , (35)

x = cosu +

where E is the observer elevation (in meters). Note that x equalsD* cosn’ whereDis the observer’s distance to the center of Earth, andn’ is the observer’s geocentric latitude.

- 3.12.4. Calculate the term y,

E

y = 0.99664719 * sinu + *sinϕ , (36)

6378140

note that y equalsD* sinn’,

- 3.12.5. Calculate the parallax in the sun right ascension, )"(in degrees),

− x*sinξ *sinH ∆α = Arctan2 ( ) . (37) cosδ− x* sinξ * cosH

Then change)"to degrees using Equation 12.

- 3.12.6. Calculate the topocentric sun right ascension "’ (in degrees), α'= α+ ∆α . (38)
- 3.12.7. Calculate the topocentric sun declination, *’ (in degrees),


(sinδ− y* sinξ ) * cos∆α δ '= Arctan2 ( ) . (39) cosδ− x* sinξ * cosH

- 3.13. Calculate the topocentric local hour angle, H’ (in degrees), H'= H − ∆α . (40)
- 3.14. Calculate the topocentric zenith angle, 2 (in degrees):


- 3.14.1. Calculate the topocentric elevation angle without atmospheric refraction correction, e0 (in degrees),

e0 = Arcsin (sinϕ *sinδ'+ cosϕ *cosδ'*cosH') . (41)

Then change e0 to degrees using Equation 12.

- 3.14.2. Calculate the atmospheric refraction correction, )e (in degrees),


P 283 102. ∆ e = * * , (42) 1010 273+ T 10.3 60*tan (e + ) 0 e0 + 511 .

Note that ∆ e = 0 when the sun is below the horizon.

where,

- - P is the annual average local pressure (in millibars).
- - T is the annual average local temperature (in /C).
- - e0 is in degrees. Calculate the tangent argument in degrees, then convert to radians if required by calculator or computer.


- 3.14.3. Calculate the topocentric elevation angle, e (in degrees),

e = e 0 + ∆e . (43)

- 3.14.4. Calculate the topocentric zenith angle, 2(in degrees), θ= 90− e . (44)


##### 3.15. Calculate the topocentric azimuth angle, M(in degrees):

- 3.15.1. Calculate the topocentric astronomers azimuth angle, '(in degrees),

sin H' Γ = Arctan2 ( ) , (45)

cosH'*sinϕ− tanδ'*cosϕ

Change'to degrees using Equation 12, then limit it to the range from 0/ to 360/ using step 3.2.6. Note that'is measured westward from south.

- 3.15.2. Calculate the topocentric azimuth angle, Mfor navigators and solar radiation users (in degrees),


Φ = Γ + 180 , (46)

Limit Mto the range from 0/ to 360/ using step 3.2.6. Note thatMis measured eastward from north.

###### 3.16. Calculate the incidence angle for a surface oriented in any direction, I (in degrees):

I = Arccos(cosθ*cosω+ sinω*sinθ*cos (Γ − γ)) , (47)

where,

- - T is the slope of the surface measured from the horizontal plane.
- - ( is the surface azimuth rotation angle, measured from south to the projection of the surface normal on the horizontal plane, positive or negative if oriented west or east from south, respectively.


###### 4. SPA Evaluation and Conclusion

Because the solar zenith, azimuth, and incidence angles are not reported in the Astronomical Almanac (AA), the following sun parameters are used for the evaluation: The main parameters (ecliptic longitude and latitude for the mean Equinox of date, apparent right ascension, apparent declination), and the correcting parameters (nutation in longitude, nutation in obliquity, obliquity of ecliptic, and true geometric distance). Exact trigonometric functions are used with the AA reported sun parameters to calculate the solar zenith and azimuth angles, therefore it is adequate to evaluate the SPA uncertainty using these parameters. To evaluate the uncertainty of the SPA, we chose the second day of each month, for each of the years 1994, 1995, 1996, and 2004, at 0hour Terrestrial Time (TT). Figures 2 shows that the maximum difference between the AA and SPA main parameters is -0.00015/. Figure 3 shows that the maximum difference between the AA and SPA for calculating the zenith or azimuth angle is 0.00003/ and 0.00008/, respectively. This implies that the SPA is well within the stated uncertainty of ± 0.0003/.

###### %

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

1.1

1.2

1.3

1.4

1.5

1.6

1.7

1.8

1.9

- 2


| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


0 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 Solar zenith angle

###### Figure 1. Uncertainty of cosine the solar zenith angle resulting from 0.01° and 0.0003° uncertainty in the angle calculation

|0.01°<br><br>0.0003°|
|---|


0.0001

| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


0.00005

0

(in°)Almanac-SPA

|Ecliptic longitude<br><br>Ecliptic latitude<br><br>Apparent right ascention<br><br>Apparent declination|
|---|


-0.00005

-0.0001

-0.00015

11

13

15

17

19

21

23

25

27

29

31

33

35

37

39

41

43

45

47

1

3

5

7

9

Day

- Figure 2. Difference between the Almanac and SPA for the ecliptic longitude, ecliptic latitude, apparent right ascension, and apparent declination on the second day of each month at 0-TT for the years 1994, 1995, 1996, and 2004


0.0001

| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


0.00005

(in°)Almanac-SPA

|Zenith<br><br>Azimuth|
|---|


0

- -0.0001
- -0.00005


11

13

15

17

19

21

23

25

27

29

31

33

35

37

39

41

43

45

47

1

3

5

7

9

Day

- Figure 3. Difference between the Almanac and SPA for the solar zenith and azimuth angles on the second day of each month at 0-TT for the years 1994, 1995, 1996, 2004


###### References

- 1. Blanco-Muriel, M., et al. “Computing the Solar Vector”. Solar Energy. Vol. 70, No. 5, 2001; pp. 431-441, 2001, Great Britain.
- 2. Michalsky, J. J. “The Astronomical Almanac’s Algorithm for Approximate Solar Position (1950-2050)”. Solar Energy. Vol. 40, No. 3, 1988; pp. 227-235, USA.
- 3. Meeus, J. “Astronomical Algorithms”. Second edition 1998, Willmann-Bell, Inc., Richmond, Virginia, USA.
- 4. Iqbal, M. “An Introduction to Solar Radiation”. New York: 1983; pp. 23-25.
- 5. The Astronomical Almanac. Norwich:2004.
- 6. The U.S. Naval Observatory. Washington, DC, http://www.usno.navy.mil/.


16

###### Appendix

Note that some of the symbols used in the appendix are independent from the symbols used in the main report.

###### A.1. Equation of Time

The Equation of Time, E, is the difference between solar apparent and mean time. Use the following equation to calculate E (in degrees),

E = M − 0.0057183− α+ ∆ψ *cosε , (A1)

where,

- M is the sun’s mean longitude (in degrees),

M = 280.4664567 + 360007.6982779* JME + 0.03032028* JME2 + JME 3 JME4 JME5 (A2)

− − , 49931 15300 2000000

where JME is the Julian Ephemeris Millennium calculated from Equation 8, and M is limited to the range from 0/ to 360/ using step 3.2.6.

- -" is the geocentric right ascention, from Equation 30 (in degrees).
- -)R is the nutation in longitude, from Equation 22 (in degrees).
- -g is the obliquity of the ecliptic, from Equation 25 (in degrees).


Multiply E by 4 to change its unit from degrees to minutes of time. Limit E if its absolute value is greater than 20 minutes, by adding or subtracting 1440.

###### A.2. Sunrise, Sun Transit, and Sunset

The value of 0.5667/ is typically adopted for the atmospheric refraction at sunrise and sunset times. Thus for the sun radius of 0.26667/, the value -0.8333/ of sun elevation (h’0 ) is chosen to calculate the times of sunrise and sunset. On the other hand, the sun transit is the time when the center of the sun reaches the local meridian.

- A.2.1. Calculate the apparent sidereal time at Greenwich at 0 UT, <(in degrees), using Equation 29.
- A.2.2. Calculate the geocentric right ascension and declination at 0 TT, using Equations 30 and 31, for the day before the day of interest (D-1), the day of interest (D0),


- α−1 δ−1 then the day after (D+1). Denote the values as α0 δ0 , in degrees. α+1 δ+1
- A.2.3. Calculate the approximate sun transit time, m0 , in fraction of day,

α0 − σ − ν

m0 = , (A3)

360

whereF is the observer geographical longitude, in degrees, positive east of Greenwich..

- A.2.4. Calculate the local hour angle corresponding to the sun elevation equals 0.8333/, H0 ,

sin h'0− sinϕ * sinδ0

H0 = Arccos ( ) , (A4)

cosϕ * cosδ0

where,

- - h’0 equals -0.8333/.
- -n is the observer geographical latitude, in degrees, positive north of the equator.


Note that if the argument of the Arccosine is not in the range from -1 to 1, it means that the sun is always above or below the horizon for that day.

Change H0 to degrees using Equation 12, then limit it to the range from 0/ to 180/ using step 3.2.6 and replacing 360 by 180.

- A.2.5. Calculate the approximate sunrise time, m1 , in fraction of day,

H0 m1 = m0 − . (A5) 360

- A.2.6. Calculate the approximate sunset time, m2 , in fraction of day,

m = m +

H0 2 0 . (A6) 360

- A.2.7. Limit the values of m0 , m1 , and m2 to a value between 0 and 1 fraction of day using step 3.2.6 and replacing 360 by 1.


###### A.2.8. Calculate the sidereal time at Greenwich, in degrees, for the sun transit, sunrise, and sunset, <i ,

νi = ν+ 360 .985647*mi , (A7) where i equals 0, 1, and 2 for sun transit, sunrise, and sunset, respectively.

###### A.2.9. Calculate the terms ni ,

∆ T ni = mi + , (A8) 86400

where)T = TT-UT.

###### A.2.10. Calculate the values "’i and *’i , in degrees, where i equals 0, 1, and 2,

where,

' ni (a + b + c*ni )

α i = α0 + 2 , (A9) and,

' ni (a'+b '+c' *ni )

δ i= δ0 + , (A10)

2

where,

- - a and a’ equal ("0 - "-1 ) and (*0 - *-1 ), respectively.
- - b and b’ equal ("+1 - "0 ) and (*+1 - *0 ), respectively.
- - c and c’ equal (b - a) and (b’ - a’), respectively.


If the absolute value of a, a’, b, or b’ is greater than 2, then limit its value between 0 and 1 as shown in step A.2.7.

###### A.2.11. Calculate the local hour angle for the sun transit, sunrise, and sunset, H’i (in degrees),

H'i = νi + σ − α'i . (A11)

H’i in this case is measured as positive westward from the meridian, and negative eastward from the meridian. Thus limit H’i between -180/ and 180/. To preserve the quadrant sign of H’i limit it to ± 360/ first, then if H’i is less than or equal -180/, then add 360/ to force it’s value to be between 0/ and 180/. And if H’i is greater than or equal 180/, then add -360/ to force it’s value to be between 0/ and -180/.

###### A.2.12. Calculate the sun altitude for the sun transit, sunrise, and sunset, hi (in degrees),

hi = A rcsin (sinϕ *sinδ'i + cosϕ *cosδ'i*cos H'i ) . (A12)

- A.2.13. Calculate the sun transit, T (in fraction of day),

H'0 T = m0 − . (A13) 360

- A.2.14. Calculate the sunrise, R (in fraction of day),

h h' R m1 + 1

− 0

= . (A14)

360*cosδ '1*cosϕ *sin H'1

- A.2.15. Calculate the sunset, S (in fraction of day), by using Equation A14 and replacing R by S, and replacing the suffix number 1 by 2.


The fraction of day value is changed to UT by multiplying the value by 24. To evaluate the uncertainty of the SPA, we chose the second day of each month, for each of the years 1994, 1995, 1996, and 2004, at 0-hour Terrestrial Time (TT). Figure A2.1 shows that the maximum difference between the AA and SPA sun transit time is -0.23 seconds. Because the sunrise and sunset are recorded in the AA to a one minute resolution, we compared the SPA calculations at only three data points at Greenwich meridian at 0-UT. The comparison result in Table A2.1 shows that the maximum difference between AA and SPA is 15.4 seconds (0.26 minute), which is well within the AA resolution of one minute. Note that UT can be changed to local time by adding the time zone as a fraction of a day (time zone is divided by 24), and limiting the result to the range from 0 to 1.

###### Table A2.1. The AA and SPA Results for Sunrise and Sunset at Greenwich Meridian at 0-UT

|Date|Observer Latitude|Sunrise| |Sunset| |
|---|---|---|---|---|---|
| | |AA|SPA|AA|SPA|
|January 2, 1994|35/|7:08|7:08:12.8|17:00|16:59:55.9|
|July 5, 1996|-35/|7:08|7:08:15.4|17:00|17:01:04.5|
|December 4, 2004|-35/|4:39|4:38:57.1|19:02|19:02:2.5|


- -0.14
- -0.15
- -0.16
- -0.17
- -0.18
- -0.19
- -0.2
- -0.21
- -0.22
- -0.23
- -0.24


| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


Day (inseconds)Almanac-SPA

11

13

15

17

19

21

23

25

27

29

31

33

35

37

39

41

43

45

47

1

3

5

7

9

Figure A2.1. Difference between the Almanac and SPA for the Ephemeris Transit on the second day of each month at 0-TT for the years 1994, 1995, 1996, 2004

A-5

###### A.3. Calculation of Calendar Date from Julian Day

- A.3.1. Add 0.5 to the Julian Day (JD), then record the integer of the result as Z, and the fraction decimal as F.
- A.3.2. If Z is less than 2299161, then record A equals Z. Else, calculate the term B,

Z − 1867216.25 B = I NT ( ) , (A15) 36524.25

Then calculate the term A,

B A = Z + 1+ B − I NT ( ) . (A16) 4

- A.3.3. Calculate the term C, C = A + 1524 . (A17)
- A.3.4. Calculate the term D,

C − 122.1 D = I NT ( ) . (A18) 365.25

- A.3.5. Calculate the term G, G = IN T (365.25* D) . (A19)
- A.3.6. Calculate the term I,

C − G I = I NT ( ) . (A20) 30.6001

- A.3.7. Calculate the day number of the month with decimals, d, d = C − G − IN T (30.6001* I) + F . (A21)
- A.3.8. Calculate the month number, m,


m = I − 1, IF I < 14 ,

###### m = I − 13 , I F I ≥ 14 .

(A22)

- A.3.9. Calculate the year, y,


###### y = D − 4716 , IF m > 2 ,

###### y = D − 4715 , IF m ≤ 2 .

(A23)

Note that if local time is used to calculate the JD, then the local time zone is added to the JD in step A.3.1 to calculate the local Calendar Date.

- A.4. Tables Table A4.1. Examples for Testing any Program to Calculate the Julian Day


|Date|UT|JD|Date|UT|JD|
|---|---|---|---|---|---|
|January 1, 2000|12:00:00|2451545.0|December 31, 1600|00:00:00|2305812.5|
|January 1, 1999|00:00:00|2451179.5|April 10, 837|07:12:00|2026871.8|
|January 27, 1987|00:00:00|2446822.5|December 31, -123|00:00:00|1676496.5|
|June 19, 1987|12:00:00|2446966.0|January 1, -122|00:00:00|1676497.5|
|January 27, 1988|00:00:00|2447187.5|July 12, -1000|12:00:00|1356001.0|
|June 19, 1988|12:00:00|2447332.0|February 29, -1000|00:00:00|1355866.5|
|January 1, 1900|00:00:00|2415020.5|August 17, -1001|21:36:00|1355671.4|
|January 1, 1600|00:00:00|2305447.5|January 1, -4712|12:00:00|0.0|


Table A4.2. Earth Periodic Terms

|Term|Row Number|A|B|C|
|---|---|---|---|---|
|L0|0|175347046|0|0|
| |1|3341656|4.6692568|6283.07585|
| |2|34894|4.6261|12566.1517|
| |3|3497|2.7441|5753.3849|
| |4|3418|2.8289|3.5231|
| |5|3136|3.6277|77713.7715|
| |6|2676|4.4181|7860.4194|
| |7|2343|6.1352|3930.2097|
| |8|1324|0.7425|11506.7698|
| |9|1273|2.0371|529.691|
| |10|1199|1.1096|1577.3435|


| |11|990|5.233|5884.927|
|---|---|---|---|---|
| |12|902|2.045|26.298|
| |13|857|3.508|398.149|
| |14|780|1.179|5223.694|
| |15|753|2.533|5507.553|
| |16|505|4.583|18849.228|
| |17|492|4.205|775.523|
| |18|357|2.92|0.067|
| |19|317|5.849|11790.629|
| |20|284|1.899|796.298|
| |21|271|0.315|10977.079|
| |22|243|0.345|5486.778|
| |23|206|4.806|2544.314|
| |24|205|1.869|5573.143|
| |25|202|2.458|6069.777|
| |26|156|0.833|213.299|
| |27|132|3.411|2942.463|
| |28|126|1.083|20.775|
| |29|115|0.645|0.98|
| |30|103|0.636|4694.003|
| |31|102|0.976|15720.839|
| |32|102|4.267|7.114|
| |33|99|6.21|2146.17|
| |34|98|0.68|155.42|
| |35|86|5.98|161000.69|
| |36|85|1.3|6275.96|
| |37|85|3.67|71430.7|
| |38|80|1.81|17260.15|
| |39|79|3.04|12036.46|
| |40|75|1.76|5088.63|
| |41|74|3.5|3154.69|
| |42|74|4.68|801.82|
| |43|70|0.83|9437.76|
| |44|62|3.98|8827.39|


| |45|61|1.82|7084.9|
|---|---|---|---|---|
| |46|57|2.78|6286.6|
| |47|56|4.39|14143.5|
| |48|56|3.47|6279.55|
| |49|52|0.19|12139.55|
| |50|52|1.33|1748.02|
| |51|51|0.28|5856.48|
| |52|49|0.49|1194.45|
| |53|41|5.37|8429.24|
| |54|41|2.4|19651.05|
| |55|39|6.17|10447.39|
| |56|37|6.04|10213.29|
| |57|37|2.57|1059.38|
| |58|36|1.71|2352.87|
| |59|36|1.78|6812.77|
| |60|33|0.59|17789.85|
| |61|30|0.44|83996.85|
| |62|30|2.74|1349.87|
| |63|25|3.16|4690.48|
|L1|0|628331966747|0|0|
| |1|206059|2.678235|6283.07585|
| |2|4303|2.6351|12566.1517|
| |3|425|1.59|3.523|
| |4|119|5.796|26.298|
| |5|109|2.966|1577.344|
| |6|93|2.59|18849.23|
| |7|72|1.14|529.69|
| |8|68|1.87|398.15|
| |9|67|4.41|5507.55|
| |10|59|2.89|5223.69|
| |11|56|2.17|155.42|
| |12|45|0.4|796.3|
| |13|36|0.47|775.52|
| |14|29|2.65|7.11|


| |15|21|5.34|0.98|
|---|---|---|---|---|
| |16|19|1.85|5486.78|
| |17|19|4.97|213.3|
| |18|17|2.99|6275.96|
| |19|16|0.03|2544.31|
| |20|16|1.43|2146.17|
| |21|15|1.21|10977.08|
| |22|12|2.83|1748.02|
| |23|12|3.26|5088.63|
| |24|12|5.27|1194.45|
| |25|12|2.08|4694|
| |26|11|0.77|553.57|
| |27|10|1.3|6286.6|
| |28|10|4.24|1349.87|
| |29|9|2.7|242.73|
| |30|9|5.64|951.72|
| |31|8|5.3|2352.87|
| |32|6|2.65|9437.76|
| |33|6|4.67|4690.48|
|L2|0|52919|0|0|
| |1|8720|1.0721|6283.0758|
| |2|309|0.867|12566.152|
| |3|27|0.05|3.52|
| |4|16|5.19|26.3|
| |5|16|3.68|155.42|
| |6|10|0.76|18849.23|
| |7|9|2.06|77713.77|
| |8|7|0.83|775.52|
| |9|5|4.66|1577.34|
| |10|4|1.03|7.11|
| |11|4|3.44|5573.14|
| |12|3|5.14|796.3|
| |13|3|6.05|5507.55|
| |14|3|1.19|242.73|


| |15|3|6.12|529.69|
|---|---|---|---|---|
| |16|3|0.31|398.15|
| |17|3|2.28|553.57|
| |18|2|4.38|5223.69|
| |19|2|3.75|0.98|
|L3|0|289|5.844|6283.076|
| |1|35|0|0|
| |2|17|5.49|12566.15|
| |3|3|5.2|155.42|
| |4|1|4.72|3.52|
| |5|1|5.3|18849.23|
| |6|1|5.97|242.73|
|L4|0|114|3.142|0|
| |1|8|4.13|6283.08|
| |2|1|3.84|12566.15|
|L5|0|1|3.14|0|
|B0|0|280|3.199|84334.662|
| |1|102|5.422|5507.553|
| |2|80|3.88|5223.69|
| |3|44|3.7|2352.87|
| |4|32|4|1577.34|
|B1|0|9|3.9|5507.55|
| |1|6|1.73|5223.69|
|R0|0|100013989|0|0|
| |1|1670700|3.0984635|6283.07585|
| |2|13956|3.05525|12566.1517|
| |3|3084|5.1985|77713.7715|
| |4|1628|1.1739|5753.3849|
| |5|1576|2.8469|7860.4194|
| |6|925|5.453|11506.77|
| |7|542|4.564|3930.21|
| |8|472|3.661|5884.927|
| |9|346|0.964|5507.553|
| |10|329|5.9|5223.694|


| |11|307|0.299|5573.143|
|---|---|---|---|---|
| |12|243|4.273|11790.629|
| |13|212|5.847|1577.344|
| |14|186|5.022|10977.079|
| |15|175|3.012|18849.228|
| |16|110|5.055|5486.778|
| |17|98|0.89|6069.78|
| |18|86|5.69|15720.84|
| |19|86|1.27|161000.69|
| |20|65|0.27|17260.15|
| |21|63|0.92|529.69|
| |22|57|2.01|83996.85|
| |23|56|5.24|71430.7|
| |24|49|3.25|2544.31|
| |25|47|2.58|775.52|
| |26|45|5.54|9437.76|
| |27|43|6.01|6275.96|
| |28|39|5.36|4694|
| |29|38|2.39|8827.39|
| |30|37|0.83|19651.05|
| |31|37|4.9|12139.55|
| |32|36|1.67|12036.46|
| |33|35|1.84|2942.46|
| |34|33|0.24|7084.9|
| |35|32|0.18|5088.63|
| |36|32|1.78|398.15|
| |37|28|1.21|6286.6|
| |38|28|1.9|6279.55|
| |39|26|4.59|10447.39|
|R1|0|103019|1.10749|6283.07585|
| |1|1721|1.0644|12566.1517|
| |2|702|3.142|0|
| |3|32|1.02|18849.23|
| |4|31|2.84|5507.55|


| |5|25|1.32|5223.69|
|---|---|---|---|---|
| |6|18|1.42|1577.34|
| |7|10|5.91|10977.08|
| |8|9|1.42|6275.96|
| |9|9|0.27|5486.78|
|R2|0|4359|5.7846|6283.0758|
| |1|124|5.579|12566.152|
| |2|12|3.14|0|
| |3|9|3.63|77713.77|
| |4|6|1.87|5573.14|
| |5|3|5.47|18849.23|
|R3|0|145|4.273|6283.076|
| |1|7|3.92|12566.15|
|R4|0|4|2.56|6283.08|


###### Table A4.3. Periodic Terms for the Nutation in Longitude and Obliquity

|Coefficients for Sin terms| | | | |Coefficients for)R| |Coefficients for),| |
|---|---|---|---|---|---|---|---|---|
|Y0|Y1|Y2|Y3|Y4|a|b|c|d|
|0|0|0|0|1|-171996|-174.2|92025|8.9|
|-2|0|0|2|2|-13187|-1.6|5736|-3.1|
|0|0|0|2|2|-2274|-0.2|977|-0.5|
|0|0|0|0|2|2062|0.2|-895|0.5|
|0|1|0|0|0|1426|-3.4|54|-0.1|
|0|0|1|0|0|712|0.1|-7| |
|-2|1|0|2|2|-517|1.2|224|-0.6|
|0|0|0|2|1|-386|-0.4|200| |
|0|0|1|2|2|-301| |129|-0.1|
|-2|-1|0|2|2|217|-0.5|-95|0.3|
|-2|0|1|0|0|-158| | | |
|-2|0|0|2|1|129|0.1|-70| |
|0|0|-1|2|2|123| |-53| |
|2|0|0|0|0|63| | | |
|0|0|1|0|1|63|0.1|-33| |
|2|0|-1|2|2|-59| |26| |


|0|0|-1|0|1|-58|-0.1|32| |
|---|---|---|---|---|---|---|---|---|
|0|0|1|2|1|-51| |27| |
|-2|0|2|0|0|48| | | |
|0|0|-2|2|1|46| |-24| |
|2|0|0|2|2|-38| |16| |
|0|0|2|2|2|-31| |13| |
|0|0|2|0|0|29| | | |
|-2|0|1|2|2|29| |-12| |
|0|0|0|2|0|26| | | |
|-2|0|0|2|0|-22| | | |
|0|0|-1|2|1|21| |-10| |
|0|2|0|0|0|17|-0.1| | |
|2|0|-1|0|1|16| |-8| |
|-2|2|0|2|2|-16|0.1|7| |
|0|1|0|0|1|-15| |9| |
|-2|0|1|0|1|-13| |7| |
|0|-1|0|0|1|-12| |6| |
|0|0|2|-2|0|11| | | |
|2|0|-1|2|1|-10| |5| |
|2|0|1|2|2|-8| |3| |
|0|1|0|2|2|7| |-3| |
|-2|1|1|0|0|-7| | | |
|0|-1|0|2|2|-7| |3| |
|2|0|0|2|1|-7| |3| |
|2|0|1|0|0|6| | | |
|-2|0|2|2|2|6| |-3| |
|-2|0|1|2|1|6| |-3| |
|2|0|-2|0|1|-6| |3| |
|2|0|0|0|1|-6| |3| |
|0|-1|1|0|0|5| | | |
|-2|-1|0|2|1|-5| |3| |
|-2|0|0|0|1|-5| |3| |
|0|0|2|2|1|-5| |3| |
|-2|0|2|0|1|4| | | |


|-2|1|0|2|1|4| | | |
|---|---|---|---|---|---|---|---|---|
|0|0|1|-2|0|4| | | |
|-1|0|1|0|0|-4| | | |
|-2|1|0|0|0|-4| | | |
|1|0|0|0|0|-4| | | |
|0|0|1|2|0|3| | | |
|0|0|-2|2|2|-3| | | |
|-1|-1|1|0|0|-3| | | |
|0|1|1|0|0|-3| | | |
|0|-1|1|2|2|-3| | | |
|2|-1|-1|2|2|-3| | | |
|0|0|3|2|2|-3| | | |
|2|-1|0|2|2|-3| | | |


- A.5. Example The results for the following site parameters are listed in Table A5.1:


- - Date = October 17, 2003. - Time = 12:30:30 Local Standard Time (LST).
- - Time zone(TZ) = -7 hours. - Longitude = -105.1786/.
- - Latitude = 39.742476/. - Pressure = 820 mbar.
- - Elevation = 1830.14 m. - Temperature = 11/C.
- - Surface slope = 30/. - Surface azimuth rotation = -10/.
- -)T = 67 Seconds. LST must be changed to UT by subtracting TZ from LST, and changing the date if necessary.


###### Table A5.1. Results for Example

|JD|2452930.312847| | |
|---|---|---|---|
|L0|172067561.526586|L1|628332010650.051147|
|L2|61368.682493|L3|-26.902819|
|L4|-121.279536|L5 -0.999999| |
|L|24.0182616917/| | |
|B0|-176.502688|B1 3.067582| |
|B|-0.0001011219/| | |
|R0|99653849.037796|R1 100378.567146| |


|R2|-1140.953507|R3|-141.115419|
|---|---|---|---|
|R4|1.232361| | |
|R|0.9965422974 AU| | |
|1|204.0182616917/|$|0.0001011219/|
|)R|-0.00399840/|)g|0.00166657/|
|g|23.440465/|8|204.0085519281/|
|"|202.22741/|*|-9.31434/|
|H|11.105900/|H’|11.10629/|
|"’|202.22704/|*’|-9.316179/|
|2|50.11162/|N|194.34024/|
|I|25.18700/|M|205.8971722516/|
|E|14.641503 minutes|Transit|18:46:04.97 UT|
|Sunrise|13:12:43.46 UT|Sunset|00:20:19.19 UT|


###### A.6. C source code for SPA

NREL has developed a C source code for the Solar Position Algorithm. It is available for download at:

http://www.nrel.gov/midc/spa/ NREL also has other related solar models and tools that might be of interest: http://www.nrel.gov/rredc/models_tools.html

|REPORT DOCUMENTATION PAGE| | |Form Approved OMB NO. 0704-0188|
|---|---|---|---|
|Public reporting burden for this collection of information is estimated to average 1 hour per response, including the time for reviewing instructions, searching existing data sources, gathering and maintaining the data needed, and completing and reviewing the collection of information. Send comments regarding this burden estimate or any other aspect of this collection of information, including suggestions for reducing this burden, to Washington Headquarters Services, Directorate for Information Operations and Reports, 1215 Jefferson Davis Highway, Suite 1204, Arlington, VA 22202-4302, and to the Office of Management and Budget, Paperwork Reduction Project (0704-0188), Washington, DC 20503.| | | |
|1. AGENCY USE ONLY (Leave blank)|2. REPORT DATE<br><br>Revised January 2008|3. REPORT TYPE AND DATES COVERED<br><br>Technical Report| |
|4. TITLE AND SUBTITLE<br><br>Solar Position Algorithm for Solar Radiation Applications| | |5. FUNDING NUMBERS<br><br>WU1D5600<br><br>|
|6. AUTHOR(S)<br><br>Ibrahim Reda & Afshin Andreas| | | |
|7. PERFORMING ORGANIZATION NAME(S) AND ADDRESS(ES)<br><br>National Renewable Energy Laboratory 1617 Cole Blvd. Golden, CO 80401-3393| | |8. PERFORMING ORGANIZATION REPORT NUMBER<br><br>NREL/TP-560-34302|
|9. SPONSORING/MONITORING AGENCY NAME(S) AND ADDRESS(ES)| | |10. SPONSORING/MONITORING AGENCY REPORT NUMBER|
|11. SUPPLEMENTARY NOTES<br><br>NREL Technical Monitor: Ibrahim Reda| | | |
|12a. DISTRIBUTION/AVAILABILITY STATEMENT<br><br>National Technical Information Service U.S. Department of Commerce 5285 Port Royal Road Springfield, VA 22161| | |12b. DISTRIBUTION CODE|
|13. ABSTRACT (Maximum 200 words)<br><br>1. This report is a step-by-step procedure for implementing an algorithm to calculate the solar zenith and azimuth angles in the period from the year –2000 to 6000, with uncertainties of ±0.0003/. It is written in a step-by-step format to simplify otherwise complicated steps, with a focus on the sun instead of the planets and stars in general. The algorithm is written in such a way to accommodate solar radiation applications.| | | |
|14. SUBJECT TERMS<br><br>algorithm; solar position algorithm; solar radiation; solar radiation applications; solar zenith angles; solar azimuth angles<br><br>| | |15. NUMBER OF PAGES|
| | | |16. PRICE CODE|
|17. SECURITY CLASSIFICATION OF REPORT<br><br>Unclassified|18. SECURITY CLASSIFICATION OF THIS PAGE<br><br>Unclassified|19. SECURITY CLASSIFICATION OF ABSTRACT<br><br>Unclassified|20. LIMITATION OF ABSTRACT<br><br>UL|


NSN 7540-01-280-5500 Standard Form 298 (Rev. 2-89)

Prescribed by ANSI Std. Z39-18 298-102

