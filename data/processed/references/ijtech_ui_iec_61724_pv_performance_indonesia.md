# A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW Crystalline-Si PV System under the Tropical Climate of Indonesia
**Rujukan Ilmiah Standar IEC 61724 & Benchmark Performance Ratio (PR) Iklim Tropis Indonesia**

- **Penulis:** Kun Kunaifi, Angele Reinders, Dimas Kaharudin, Aripriantoni Harmanto, Kirjono Mudiarto
- **Afiliasi:** University of Twente (Belanda), UIN Suska Riau, Eindhoven University of Technology, PT Pembangkitan Jawa-Bali (PJB / PLN Group)
- **Jurnal Resmi:** *International Journal of Technology* (IJTech), Universitas Indonesia, Vol. 10(6): 1082-1092 (2019)
- **ISSN:** 2086-9614 | **DOI:** [10.14716/ijtech.v10i6.3612](https://doi.org/10.14716/ijtech.v10i6.3612)
- **Berkas Bukti Fisik:** `data/raw/sources/ijtech_ui_iec_61724_pv_performance_indonesia.pdf`

---

## Verbatim Text Ekstraksi Dokumen Asli (Per Halaman)


### Halaman 1

```text
International Journal of Technology 10(6): 1082-1092 
ISSN 2086-9614 
© IJTech 2019 
 
 
 
A COMPARATIVE PERFORMANCE ANALYSIS OF A 1 MW CIS PV SYSTEM 
AND A 5 KW CRYSTALLINE-SI PV SYSTEM UNDER THE TROPICAL 
CLIMATE OF INDONESIA 
 
Kun Kunaifi 1,2*, Angèle Reinders1,3, Dimas Kaharudin4, Aripriantoni Harmanto4,  
Kirjono Mudiarto4 
 
1Department of Design, Production and Management, Faculty of Engineering Technology, 
University of Twente, Enschede, The Netherlands 
2UIN Sultan Syarif Kasim Riau University, Pekanbaru, Indonesia 
3Energy Technology Group, Department of Mechanical Engineering, Eindhoven University of 
Technology, Eindhoven, The Netherlands 
4PT. Pembangkitan Jawa-Bali, Jl. Ketintang Baru No. 11 Surabaya, Indonesia 
 
(Received: August 2019 / Revised: October 2019 / Accepted: October 2019) 
 
ABSTRACT 
Despite being a tropical country with great potential for solar power, knowledge about the actual 
performance of photovoltaic (PV) systems in Indonesia remains limited. In this paper, using 5-
minute resolution data from 2016 to 2018 obtained from a 1 MW Copper Indium Selenide (CIS) 
and a 5 kW crystalline silicon (c-Si) PV plant in West Java, we aim to answer the question of how 
a CIS PV plant performs and degrades in Indonesia’s tropical climate and how it compares to a 
PV system that contains c-Si technology. The methodological approach used includes 
performance analyses of these PV systems according to IEC standard 61724 and an investigation 
of the degradation rate using NREL/RdTools. The following results were derived from the 
analyses: the total annual Hi was 1500 kWh/m2 or around 4.2 kWh/m2/day. The daily-averaged 
performance ratio, PR, was 91.7 % ± 4 % and 87.4 % ± 7 % for the CIS system with string 
inverters and a central inverter, respectively. The mean PR of the CIS systems was 12 % higher 
than that of the c-Si system, which was 79.8 %. Concerning the final yield, Yf, the CIS system 
with a mean Yf of 3.85 kWh/kWp outperformed the c-Si system by 14 %. The CIS system 
degraded by 1.53 % per year, which is less than the c-Si system with a degradation rate (Rd) of 
3.72 % per year. From these results, it can be concluded that, in this case, CIS technology 
performs better than c-Si in Indonesia’s tropical climate. Uncertainties in the calculation and high 
values of Rd could be areas for further investigation. 
 
Keywords:  Degradation; Indonesia; Performance; PV systems; Tropical climate 
 
1. INTRODUCTION 
Indonesia has many rural areas and remote islands that are suitable for distributed renewable 
power generation such as solar photovoltaic (PV) systems. PV systems are reliable power 
systems and play an essential role in climate change mitigation (Creutzig et al., 2017). The 
market for PV systems is beginning to grow rapidly worldwide owing to, among other factors, 
their increased efficiency, the increased lifespans of the components, and a rapid reduction in 
their cost (Fraunhofer ISE, 2019). 
*Corresponding author’s email: k.kunaifi@utwente.nl, Tel. +31534892264 
Permalink/DOI: https://doi.org/10.14716/ijtech.v10i6.3612
```


### Halaman 2

```text
Kunaifi et al. 
1083 
The first PV system applications in Indonesia can be traced back to 1978 and the installation of a  5 
kWp solar water pumping system (Dasuki et al., 2001). Various other projects then followed, such 
as a solar home systems (SHS) pilot project (Reinders et al., 1999), desalination plants, basic medical 
applications, remote televisions, and water pumping systems (Veldhuis & Reinders, 2015). A large 
SHS demonstration project with a total capacity of 50 MWp was launched in 1994 (Veldhuis & 
Reinders, 2015), and the first urban PV system was introduced in 2003 (Ministry of Energy and 
Mineral Resources, 2012). 
Since then, many other PV systems have been constructed and created employment (Elfani, 2011). 
However, it is only relatively recently that Indonesia has gained experience in the performance of 
PV systems (Kunaifi & Reinders, 2018), and it continues to be in the research and demonstration 
phase (Veldhuis & Reinders, 2015). To date, Indonesia has 12 utility-scale PV plants in operation, 
mainly for off-grid or industrial applications. The dominant PV technology applied is typically 
crystalline silicon (c-Si) technology.  
The PV market in Indonesia is emerging and is expected to grow over the coming years across 
the vast expanse of Indonesia’s archipelago. The factors driving its growth include Indonesia’s 
unique geography, comprising six large and more than 17 thousand smaller islands. This type of 
geographical factor presents a challenge in terms of extending the conventional power grid to 
reach the whole of the country’s population of more than 260 million. The other motivations for 
solar electrification in Indonesia include, among others, the increasing demand for electricity 
(around 5.5 % annual growth) and economic growth of 5 % per year.  
PV systems are suitable for use on the large islands (urban areas), particularly with respect to 
increasing the quality of the power supply (Nazir et al., 2016) as Indonesia is characterized by the 
relatively low reliability of its electricity supply (Kunaifi & Reinders, 2018). Meanwhile, on the 
smaller islands and in more remote areas, PV systems could play a significant role in providing 
electricity to local people who have not had it before, replacing fossil-fuel-generated electricity 
with renewables, and increasing the electrification ratio (PLN, 2018). 
It is essential to monitor the operation of a PV system in order to identify performance trends. 
Monitoring data is also crucial for the localization of potential faults and to enable a comparison 
of PV system performance against design expectations and guarantees and between the different 
configurations and locations (The International Electrotechnical Commission, 2017). However, 
most PV systems in Indonesia are not monitored, with only a few equipped with basic 
monitoring systems. Accordingly, we have limited knowledge about the actual performance of 
PV systems operating under real environmental conditions in Indonesia. The two PV systems 
presented in this paper are among the few that are monitored. 
 
Figure 1 Aerial view of the 1 MW PV plant in Cirata, West Java, Indonesia (Photo: PJB Cirata).
```


### Halaman 3

```text
1084 
A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW  
Crystalline-Si PV System under the Tropical Climate of Indonesia 
In September 2015, PT. Pembangkitan Jawa-Bali (PJB), a subsidiary of PLN, Indonesia’s state-
owned utility company, commenced its entry into the PV business. PJB is a power generation 
company that operates mainly in Java and Bali, which are the islands with the largest and densest 
electrical power systems in Indonesia. PJB constructed and now operates and maintains nine 
power plants with a total capacity of more than 7 GW (PJB, 2019). Among those in operation 
by PJB is a 1 MW PV system located in the province of West Java, which at the time of its 
construction was the largest PV system on the island of Java (Figure 1). At the same location, 
PJB also installed other, smaller PV systems. After three years of operation, we can now, for the 
first time, analyze the monitoring data from the PV systems in West Java.  
In this paper, we therefore seek to answer the following questions: 
 How is PJB’s 1 MW CIS-based thin-film plant performing, and how has it degraded in 
Indonesia’s tropical climate? 
 How do its performance and degradation compare to that of a 5 kW crystalline (c-Si) plant at 
the same location?  
The motivation for analyzing the performance and degradation of PV systems lies in the fact 
that the long-term performance and stability of PV plants have a significant impact on the 
economics of such projects. 
Besides performance, degradation is one of the most critical characteristics to consider in the solar 
PV business. Degradation describes the rate at which a PV module experiences a decline in output. 
The degradation rate, Rd, is therefore the rate at which the PV performance of a module decreases 
per year. Rd is an important measure for comparing the actual performance of PV systems against 
the PV performance warranty issued by the module manufacturer with respect to nominal power.  
PV cells degrade (Meyer & van Dyk, 2004); however, the rate of degradation differs from one 
PV plant to another. Over the course of a 25-year operating life, a 20 % decline is considered a 
failure. Assuming linear degradation, an Rd greater than 0.8 % per year can be regarded as a 
problem (John et al., 2018). For a high-efficiency module, however, 50 % degradation may be 
acceptable (Jordan & Kurtz, 2013). Using data from outdoor field testing, the long-term behavior 
and lifetime of PV modules, including their degradation, can be quantified. 
 
2. 
THE PV SYSTEMS AND DATASETS 
The PV systems presented in this paper are located in the Village of Cadas Sari (6º674 'S, 
107º355 'E), Cirata, the province of West Java. They comprise a 1 MW and a 5 kW system. The 
1 MW plant is ground-mounted over an area of 0.9 ha, while the 5 kW plant is a rooftop PV 
installation. Both systems sit in open spaces that are free of shading throughout the year. The 
measurement equipment is not cleaned and calibrated. Therefore, rather than using the most 
recent data, we instead use two years of usable data with a starting date close to the system’s 
commencement of operation, based on the assumption that the sensors performed better during 
their earlier operational period than more recently. 
2.1. 1 MW Thin-Film CIS PV System 
 
The 1 MW PV plant has 170 Wp Japanese Solar Frontier thin-film PV modules made of Copper 
Indium Selenide (CIS) technology with a nominal module efficiency, ηmod, of 13.8 %. This 
efficiency is derived from the module’s specification sheet. It has two clusters. One cluster has 
a capacity of 530.4 kW and comprises 26 arrays, each with 120 modules. This cluster has an 
SMA 550 kW central inverter that delivers AC power to the grid through a transformer. The 
other cluster, with a total capacity of 510 kW, comprises 25 arrays, each containing 120 
modules. Each array is connected to an SMA 20 kW string inverter. The PV modules are tilted 
10º, which is an optimum angle for Indonesia (Setiawan & Setiawan, 2017), and have an
```


### Halaman 4

```text
Kunaifi et al. 
1085 
azimuth angle of 15º clockwise from the North.  
The monitoring system measured both electrical and meteorological variables at 5-minute 
intervals over the course of two years between 2016 and 2018. The electrical parameters 
(inverter-based) include DC current (Idc) in Amperes, DC voltage (Vdc) in Volts, DC power (Pdc) 
in Watts, Iac in Amperes, Vac per line in Volts, AC power (Pac) in Watts, power frequency in 
Hertz, and cumulative energy production (Eout) in kWh. There were no data for the months of 
October 2017 and February 2018. To compensate for these missing data, and in order to ensure 
two full years’ analysis, we used data from 11 March 2016 to 10 May 2018. The total number 
of daytime records was 95,546, 9 % of which were missing or were removed due to outliers, or 
were wrong, with abnormal values resulting in a monitoring faction (MF) of 0.91. 
As the 1 MW CIS system consists of two separate clusters, we analyzed each cluster 
individually. For the cluster with a central inverter, we use the term CIS Central (CISC), and for 
the cluster with string inverters, the name CIS String (CISS) is used. The PV module and 
configuration specifications are shown in Table 1. 
 
Table 1 Specifications of the PV modules in Cirata 
PV Module 
CIS 
pc-Si 
Manufacturer 
Solar Frontier, Japan 
Victron Energy (cells),  
Azet (module assembling) 
Model 
SFSF170-S 
ASL-M100E 
Pmax (Wp) 
170 
100 
VOC (V) 
112 
22.3 
VMPP (V) 
87.5 
18.0 
ISC (A) 
2.2 
6.00 
IMPP (A) 
1.95 
5.60 
Efficiency 
0.138 
NA 
Tcoeff,Pmax (%/K) 
-0.31 
-0.48 
Tcoeff,Isc (%/K) 
0.01 
0.037 
Tcoeff,Voc (%/K) 
-0.30 
-0.34 
NOCT (°C) 
47 
NA 
Length (mm) 
1,257 
1,000 
Width (mm) 
977 
670 
2.2. 5 kW Crystalline PV System 
The 5 kW PV plant has 100 Wp poly-crystalline modules that use Victron Energy solar cells 
assembled into PV modules by an Indonesian company named Azet. It is connected to the local 
grid through an SMA Sunny Mini Central 5000 inverter. The PV modules are mounted on a 
building rooftop with a tilt angle of 10º and an azimuth angle of 15º clockwise from the North. 
The monitoring system measures similar parameters to those of the CIS PV system and features 
the same recording interval of 5 minutes. 
For both the CIS and c-Si systems, critical meteorological variables were measured. They 
include relative humidity (RH ) as a percentage, ambient temperature (Ta) in ºC, module 
temperature (Tm) in ºC, global horizontal irradiance (Gh) in Watt/m2, global in-plane irradiance 
(Gi) in Watt/m2, and wind speed (v) at a 1-metre height in m/s. Table 2 shows the PV module 
and configuration specifications.
```


### Halaman 5

```text
1086 
A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW  
Crystalline-Si PV System under the Tropical Climate of Indonesia 
3. 
METHODS   
All of the monitoring data were checked for consistency and gaps to identify anomalies 
according to the following method. The daytime data were selected by eliminating irradiance 
values below 200 W/m2 and above 1,500 W/m2. For the ambient temperature, Ta, only values 
between -40 and 60 ºC were used. For the module temperature, Tm, values between the ambient 
temperature and ambient temperature plus 40 ºC were included. As such, any Tm values lower 
than Ta that might occur in the early morning due to irradiation to the sky were excluded from 
the analysis. For the electrical data, the array voltage between 0 and 1.3 x Voc,stc was used. Also, 
the array current values outside 0 and 1.5 x Isc,stc were excluded from the analysis. Abnormal 
data, such as large negative values and dead values that stuck for more than one hour, were also 
removed. Any records missing from the 5-minute data for a period of up to one hour were 
linearly interpolated. 
3.1.  Performance Calculations 
The monitoring standard IEC 61724 was applied to the analysis of the PV systems’ performance 
(The International Electrotechnical Commission, 2017). The performance indicators presented 
include final yield (Yf) in kWh/kWp; array yield (YA) in kWh/kWp; reference yield (Yr) in 
kWh/kWp; capture losses (LC) in kWh/kWp; system losses (LS) in kWh/kWp; performance ratio 
(PR) as a percentage or a decimal between 0 and 1; efficiencies (η) as a percentage or a decimal 
between 0 and 1; and capacity factor (CF), also given as a percentage.  
Yield refers to the ratio of an energy quantity to the array power rating, Prated, of the installed 
PV array at standard test conditions (STC) of 1,000 W/m2 solar irradiance and 25 °C cell 
temperature. Thus, yields indicate the actual operation of the array relative to its rated capacity. 
The unit of yield is kWh/kW. The ratio of unit is equivalent to hours, and the yield ratio indicates 
the equivalent amount of time for which the array would be required to operate at Prated to 
provide the particular energy quantity measured during the reporting period. 
The final yield, Yf, is defined as the annual, monthly, or daily net AC energy output in kWh, Eac, 
of the PV system per installed rated power, Prated, and is given by Equation 1. The final yield can 
be used to compare PV plants with different systems operating in different climates. 
 
Yf = 
Eac
Prated (
kWh
kW )  
(1) 
The array yield, YA, is defined as the amount of array energy produced, Edc, from each installed 
rated power, Prated, over the analysis period, as defined by Equation 2. It is equivalent to the 
number of hours over which the PV array produces its rated power. The unit of YA is kWh/kWp. 
 
YA = 
Edc
Prated (
kWh
kW ) 
(2) 
The reference yield in kWh/kWp, Yr, is the total amount of available in-plane solar irradiance in 
kWh/m2, Hi, divided by the reference irradiance, Gi,ref, of 1,000 W/m2 (Equation 3). 
 
Yr = 
Hi
Gi,ref (
kWh
kW ) 
(3) 
If the reporting period is equal to one day, then Yr would be the equivalent number of sun hours 
at the reference irradiance per day. 
Normalized yield losses are calculated by subtracting yields. The yield losses also have units of 
kWh/kW or hour (h). They represent the amount of time for which the array would be required 
to operate at its rated power, Prated, to provide for the respective losses during the reporting 
period. Two types of losses can be calculated once the yields have been determined. These are 
capture losses, LC, and system losses, LS.
```


### Halaman 6

```text
Kunaifi et al. 
1087 
LC represents the losses incurred due to the array operating below what would be expected in 
STC. Losses are typically caused by the effect of temperature, high incidence angles, shading, 
array circuit losses, including mismatch, low irradiance, and soiling of the array (Pryor et al., 
2013). LC is defined by Equation 4. 
 
LC = Yr - YA (
kWh
kW ) 
(4) 
LS represents the losses in the balance of system (BOS) components, including the inverter and 
all wiring and junction boxes. LS is defined by Equation 5. 
 
LS = YA - Yf = 
Edc - Eac
Prated  (
kWh
kW ) 
(5) 
PR is a useful metric that shows how closely a PV system is operating in relation to its ideal 
rated operation. PR indicates the total losses from the system output due to both array 
temperature and system component inefficiencies or failures, including the BOS components. 
The array-level performance ratio, PRA, and the system level, PR, are defined by Equation 6 and 
Equation 7. PRA is the ratio of the actual energy produced by the PV array to the available solar 
energy that can be produced from the PV array at STC efficiency. PR is the ratio of actual energy 
output to the available solar energy that can be produced from the PV array at STC 
efficiency. The PR is either unitless or it can be represented as a percentage. 
 
PRA = 
YA
Yr (dimensionless) 
(6) 
 
 
PR = 
Yf
Yr (dimensionless) 
(7) 
The efficiency, η, of a PV system can be calculated as rated array efficiency, ηA,rated, mean actual 
array efficiency, ηA, mean system efficiency, ηf, and inverter efficiency, ηinv, using Equation 8 to 
Equation 11. 
 
ηA,rated = 
Prated
Gi,ref x A  (dimensionless) 
(8) 
 
 
ηA = 
Edc
Hi x A  (dimensionless) 
(9) 
 
 
ηf = 
Eac
Hi x A  (dimensionless) 
(10) 
 
 
ηinv = 
Eac
Edc  (dimensionless) 
(11) 
where A is the effective PV module area in m2. 
Finally, CF is defined as the ratio of the actual annual energy output, Eac, to the amount of energy 
the PV system would generate if it operated at full Prated for 24 h per day for a year. CF is 
calculated using Equation 12. 
 
CF = 
Eac ACrating
⁄
24 x days  (dimensionless) 
(12) 
where ACrating, in kW, is calculated from the sum of the inverter ratings, and the term days is 
typically 365 or 366 for one year of analysis. 
3.2. Degradation Calculations 
For the Rd calculation, NREL/RdTools (Jordan et al., 2018; NREL, 2018) was implemented 
using Python. RdTools is a set of algorithms for calculating the Rd of PV systems based on year-
on-year (YOY) analysis using a minimum of two years’ time-series data (Jordan et al., 2018).
```


### Halaman 7

```text
1088 
A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW  
Crystalline-Si PV System under the Tropical Climate of Indonesia 
RdTools was developed according to the method initially proposed by Hasselbrink et al. 
(Hasselbrink et al., 2013) based on a review of 3 million module-years of live site data. Using 
RdTools, PV system production data are evaluated over several years to obtain rates of 
performance degradation over time. RdTools features an improvement in degradation analysis 
in that it avoids errors due to irradiance sensor drift, calibration, soiling, or misalignment using 
the clear-sky method; however, this is outside the scope of this study. 
Within RdTools, the computation of the degradation rates from time-series data follows three 
main steps: normalization, filtering, and data analysis (Jordan et al., 2017). The normalization 
step involves the calculation of the PR metric normalized by temperature to generate a 
temperature-corrected PR using Equation 13. 
                                           PR = 
P
Prated * Gi
Gi,ref * ( 1+ γ * [ Tcell - Tref ] )  (dimensionless) 
(13) 
where P is the measured dc power (Pdc) or ac power (Pac) of the PV system in watts, γ is the 
maximum power temperature coefficient in relative %/K, Tcell is the cell temperature in °C, and 
Tref is the reference temperature in °C with the value of 25 °C for STC or annual-averaged 
temperature. 
In the filtering step, biasing and nonrepresentative data were removed, as well as data recorded 
at times when the solar resource was poor or variable. A low irradiance cutoff of 200 W/m2 was 
applied in order to exclude start-up irradiance without removing winter data from high-latitude 
locations. We filtered out data during high dc/ac ratio in which power was >99 % of the 
maximum value. Finally, data outside of a ± 30 % band around a three-month rolling median 
performance index were also excluded. 
The final step, data analysis, involved the calculation of Rd using the remaining data based on 
three approaches. First, for the YOY method, the rate of change was computed between two 
points at the same time in subsequent years. This resulted in a histogram of rates of change, the 
central tendency of which represented the overall system performance. Second, standard least 
squares (SLS) regression, in contrast, used all data points in a single regression by minimizing 
the difference between the model and the data. Finally, quantile regression used quantiles instead 
of the response mean. Prior to analysis of the degradation, the normalized, filtered 15-min data 
were aggregated over a variable period. Further details on the degradation rate analysis 
methodology are available in (Hasselbrink et al., 2013) or (Jordan et al., 2017). 
 
4. 
RESULTS  
4.1.  System Performances 
The performance analysis covered the evaluation of the solar irradiance on-site and the energy 
produced by the PV system over time. The mean and maximum daytime values of Gi on a surface 
tilted 10º during the analysis period were 410 W/m2 and 1,250 W/m2, respectively. Figure 2a 
shows the Gi for the PV array tilted angle in Cirata during the analysis period. As shown, the 
majority of Gi values were in the range from 250 W/m2 to 800 W/m2, although a significant 
frequency of Gi below 250 W/m2 was also observed.  
The total annual Hi was 1,500 kWh/m2, with the highest value of 143.5 kWh/m2 in August (hot 
season) and the lowest value of 90.3 kWh/m2 in February (rainy season) (Figure 2b). The 
monthly average Hi was 125 ± 15 kWh/m2 or around 4.2 kWh/m2/day. The monthly-averaged 
Tm ranged from 39 0C to 43 0C (Figure 2b). However, with a data resolution of 5 minutes, Tm 
ranged from 21 0C to 68 0C. 
During the reporting period, the energy amounts supplied to the grid from the CIS and c-Si PV 
plants were resp. 1,258 MWh (≈3.4 MWh/day) and 6,012 kWh (≈16.5 kWh/day). The average
```


### Halaman 8

```text
Kunaifi et al. 
1089 
daily Yf was 3.66 kWh/kWp for CISS, 3.84 kWh/kWp for CISC, and 3.31 kWh/kWp for the c-Si 
system. In general, the Yf values of the PV systems in Cirata were high, thus demonstrating the 
significant potential of PV systems in Indonesia (Kunaifi & Reinders, 2017). 
 
 
(a) 
(b) 
Figure 2 Meteorological variables in Cirata. (a) Frequency distribution of in-plane irradiance, (b) total 
monthly irradiation and PV module temperature during daytime hours 
 
Figure 3 shows the PR of the PV systems in Cirata. The daily-averaged PR values for the CISS 
and CISC systems during the reporting period were 91.7 % ± 4 % and 87.4 % ± 7 %, respectively. 
The CISC system has a higher LC and LS than the CISS system, which created a significant 
difference in PR between the two CIS systems. PR for the c-Si system was 79.8 % ± 4 %. Table 
2 shows the main performance indicators of the three PV systems in Cirata. Using the mean 
values from CISC and CISS, it can be seen that the CIS system performed better than the c-Si 
system. The Yf of CIS was 14.1 % higher than that of the c-Si, which confirms the finding from 
a recent study (Honrubia-Escribano et al., 2018). 
 
 
Figure 3 Performance ratios of the PV systems in Cirata; green for CISC, orange for CISS, and 
magenta for c-Si 
 
The most significant difference between the two systems concerns the losses, where the c-Si 
system yielded a 47 % higher Lc and a 45 % higher Ls than the CIS. One of the reasons for the 
lower losses in the CIS systems is the higher frequency of module cleaning compared to the c-
Si system. The values for ηA,rated of the CIS and c-Si system were respectively 13.8 % and 14.9 
%. The annual-averaged CF was 16.3 % for CISS, 16.0 % for CISC, and 14.1 % for the c-Si 
system.
```


### Halaman 9

```text
1090 
A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW  
Crystalline-Si PV System under the Tropical Climate of Indonesia 
4.2. 
Degradation Rates 
Figure 4 shows the Rd of the PV systems in Cirata based on data from April 2016 to July 2018. 
The degradation rate is a rate of change, with a negative rate representing a decrease in 
performance. For the CIS system, the calculation is based on the power produced by the central 
inverter (CISC). The calculation shows that the c-Si system degraded at an average of 3.72 % 
per year, which is faster than the CIS system with its annual Rd of 1.53 %. The values for the 
confidence interval of the Rd of the CIS and c-Si system were 0.87 % to 2.06 % per year and 
2.98 % to 4.31 % per year, respectively. 
 
Table 2 Performance indicators of PV systems in Cirata 
Indicators 
Unit 
510 kW 
(CISS) 
532.4 kW 
(CISC) 
5 kW 
(c-Si) 
CIS/c-Si 
(%) 
Yf 
kWh/kWp  
3.92 
3.77 
3.37 
14.09 
YA 
kWh/kWp 
4.00 
3.91 
3.58 
10.47 
Yr 
kWh/kWp 
4.27 
4.32 
4.22 
1.78 
Lc 
kWh/kWp 
0.27 
0.41 
0.64 
-46.88 
Ls 
kWh/kWp 
0.08 
0.15 
0.21 
-45.24 
PR 
% 
91.7 
87.4 
79.8 
12.22 
ηA,rated 
% 
13.8 
13.8 
14.9 
-7.38 
ηA 
% 
13.0 
12.6 
12.7 
0.79 
ηf 
% 
12.7 
12.1 
11.9 
4.20 
ηinv 
% 
97.8 
96.2 
94.0 
3.19 
CF 
% 
16.3 
16.0 
14.1 
14.54 
 
The maintenance practices applied to the PV modules and measurement equipment can 
introduce uncertainties that result in high values of degradation. The measurement equipment in 
the PV systems in Cirata was not cleaned and calibrated, the CIS PV modules were sometimes 
cleaned, and the c-Si PV modules were never cleaned during their operation. Soiling and drifting 
of the irradiance sensors increase the uncertainty of the Rd calculation, which is an interesting 
topic for further investigation. 
 
(a)
 
(b)
 
Figure 4 The annual degradation rate of the PV systems in Cirata: (a) CISC system, (b) c-Si system
```


### Halaman 10

```text
Kunaifi et al. 
1091 
The degradation rates of the PV systems in Cirata at module level were higher than those reported 
in the literature, where the average degradation rates for silicon and thin-film technology are 
respectively 0.7 % and 1.5 % per year. However, when looking at the system level, the Rd values 
from Cirata are within the boundaries as presented in other literature (Jordan & Kurtz, 2013). 
For silicon technology, the average rate of degradation at module level is 0.5 %/year. However, 
it is possible for the rate of system degradation to reach 2.5 %/year. This also indicates that BOS 
and soiling affect degradation (Jordan & Kurtz, 2013). For the CIS module, the examination of 
yields from NREL found that the Rd of CIS can range from moderate, at 2 % to 4 % per year, to 
negligible or small, at less than 1 %/year (Del Cueto et al., 2008).  
 
5. 
CONCLUSION 
We compared the performance and degradation rate of a 1 MW CIS PV system and a 5 kW 
crystalline-Si PV system operating in the real tropical climate of Indonesia. Concerning the Yf, 
the CIS system outperformed the c-Si system by 14 %. The daily-averaged PR of the CIS system 
was 89.6 % (mean PR of the central and string clusters), which is 12.2 % higher relative to the 
PR of the c-Si system of 80 %. 
Based on monitored Pac, the Rd of the PV systems in Cirata at the module level was high. The 
CIS system degraded by 1.53 % per year, while the Rd of the c-Si system was 3.72 % per year. 
However, at the system level, the Rd values were within acceptable boundaries. By considering 
the other technical performance indicators, it can be concluded that CIS technology performs 
better than c-Si in Indonesia’s tropical climate. However, there may be some uncertainty with 
respect to the calculation of the Rd. Such uncertainties are caused by soling and the relatively 
short two-year monitoring period.  
 
6. 
ACKNOWLEDGEMENT 
We appreciate the financial support from the Indonesia Endowment Fund for Education (LPDP) 
and the expert support from Advanced Research on Innovations in Sustainability and Energy 
(ARISE) of the University of Twente. Thanks to COST Action PEARL PV for the Short Term 
Scientific Mission (STSM) grant at Eurac Research in Bolzano, Italy. 
 
7. 
REFERENCES 
Creutzig, F., Agoston, P., Goldschmidt, J.C., Luderer, G., Nemet, G., Pietzcker, R.C., 2017. The 
Underestimated Potential of Solar Energy to Mitigate Climate Change. Nat. Energy, 
Volume 2(9), doi:10.1038/nenergy.2017.140 
Dasuki, A.S., Djamin, M., Lubis, A.Y., 2001. The Strategy of Photovoltaic Technology 
Development in Indonesia. Renewable Energy, Volume 22(1-3), pp. 321–326 
Del Cueto, J.A., Rummel, S., Kroposki, B., Osterwald, C., Anderberg, A., 2008. Stability of 
CIS/CIGS Modules at the Outdoor Test Facility Over Two Decades. In: IEEE Photovoltaic 
Specialist Conference held May 11-16 
Elfani, M., 2011. The Impact of Renewable Energy on Employment in Indonesia. International 
Journal of Technology, Volume 2(1), pp. 47–55 
Fraunhofer ISE, 2019. Photovoltaics Report 2019. Freiburg 
Hasselbrink, E., Anderson, M., Defreitas, Z., Mikofski, M., Shen, Y.C., Caldwell, S., Terao, A., 
Kavulak, D., Campeau, Z., Degraaff, D., 2013. Validation of the PVLife Model using 3 
Million Module-years of Live Site Data. In: Conference Record of the IEEE Photovoltaic 
Specialists Conference, Tampa, FL, USA  
Honrubia-Escribano, A., Ramirez, F.J., Gómez-Lázaro, E., Garcia-Villaverde, P.M., Ruiz-
Ortega, M.J., Parra-Requena, G., 2018. Influence of Solar Technology in the Economic
```


### Halaman 11

```text
1092 
A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW  
Crystalline-Si PV System under the Tropical Climate of Indonesia 
Performance of PV Power Plants in Europe. A Comprehensive Analysis. Renewable 
Sustainable Energy Reviews, Volume 82, pp. 488–501 
John, J.J., Alnuaimi, A., Elnosh, A., Stefancich, M., Banda, P., 2018. Estimating Degradation 
Rates from 27 Different PV Modules Installed in Desert Conditions using the NREL/Rdtools. 
In: 2018 IEEE 7th World Conference on Photovoltaic Energy Conversion, WCPEC 2018 - A 
Joint Conference of 45th IEEE PVSC, 28th PVSEC and 34th EU PVSEC, USA 
Jordan, D.C., Deceglie, M.G., Kurtz, S.R., 2017. PV Degradation Methodology Comparison - 
A Basis for a Standard. In: IEEE 44th Photovoltaic Specialists Conference (PVSC), USA 
Jordan, D.C., Deline, C., Kurtz, S.R., Kimball, G.M., Anderson, M., 2018. Robust PV Degradation 
Methodology and Application. IEEE Journal of Photovoltaics, Volume 8(2), pp. 525–531 
Jordan, D.C., Kurtz, S.R., 2013. Photovoltaic Degradation Rates - An Analytical Review. 
Progress in Photovoltaics Research and Applications, Volume 21, pp. 12–29 
Kunaifi, K., Reinders, A.H.M.E., 2017. Estimating the Technical Potential of Grid-connected 
PV Systems in Indonesia: A Comparison of a Method based on Open Access Data with a 
Method based on GIS. In: 33rd European Photovoltaic Solar Energy Conference and 
Exhibition. WIP Renewable Energies, Amsterdam, pp. 2652–2658 
Kunaifi, K., Reinders, A.H.M.E., 2018. Performance of a Remote Hybrid PV System based on 
Real and Modelled Data in Indonesia. In: The 35th European Photovoltaic Solar Energy 
Conference and Exhibition (EU-PVSEC), At Brussels, Belgium, pp. 2060–2065 
Kunaifi, Reinders, A., 2018. Perceived and Reported Reliability of the Electricity Supply at 
Three Urban Locations in Indonesia. Energies, Volume 11(1), pp. 1–24 
Meyer, E.L., van Dyk, E.E., 2004. Assessing the Reliability and Degradation of Photovoltaic 
Module Performance Parameters. IEEE Transactions on Reliability, Volume 53(1), pp. 83–92 
Ministry of Energy and Mineral Resources, 2012. Solar Energy in Indonesia: Potentials, 
Plannings and Framework Conditions. Berlin 
Nazir, R., Nurdin, M., Fitrianto, E., 2016. Voltage Profile Improvement of the 20 kV Painan 
Distribution System with Multiple Distributed Renewable Energy Generation. 
International Journal of Technology, Volume 7(1), pp. 26–37 
NREL, 2018. RdTools version 1.2.2 
PJB, 2019. PJB Unit Pembangkitan. Available Online at https://www.ptpjb.com/unit-
pembangkitan/, Accessed on May 29, 2019 
PLN, 2018. Statistik PLN 2017. Perusahaan Listrik Negara (PLN), Jakarta, Indonesia 
Pryor, T., Watt, M., Watt, M., 2013. Australian Technical Guidelines for Monitoring and 
Analysing Photovoltaic Systems Version 1. Australian PV Institute 
Reinders, A., Sudradjat, A., Dijk, V. Van, Mulyadi, R., Turkenburg, W., 1999. Sukatani 
Revisited: On the Performance of Nine-year-old Solar Home Systems and Street Lighting 
Systems in Indonesia. Renewable Sustainable Energy Reviews, Volume 3(1), pp. 1–47 
Setiawan, A., Setiawan, E.A., 2017. Optimization of a Photovoltaic Power Plant in Indonesia 
with Proper Tilt Angle and Photovoltaic Type using a System Advisor Model. International 
Journal of Technology, Volume 8, pp. 539–548 
The International Electrotechnical Commission, 2017. IEC 61724-1 Photovoltaic System 
Performance – Part 1: Monitoring 
Veldhuis, A.J., Reinders, A.H.M.E., 2015. Reviewing the Potential and Cost-effectiveness of 
Off-grid PV Systems in Indonesia on a Provincial Level. Renewable Sustainable Energy 
Reviews, Volume 52, pp. 757–769
```
