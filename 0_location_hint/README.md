This directory is used to build our Location Hint Dictionary.

**Note: For convenience, we refer to 'country/region' as 'country'! This project has nothing to do with politics. If you feel offended by any part of this project, please do not hesitate to contact us!**

### The files in `src`

| file                | note                                                         |
| ------------------- | ------------------------------------------------------------ |
| blacklists          | The files in this directory contains the word cannot be used as a location hint. For example, such as `normal` and `sunrise`. Thanks to https://github.com/tumi8/hloc, it helps me find a lot of words. I also add some other words by myslef. |
| pages_offline       | This directory contains the webpages content of https://www.world-airport-codes.com. We get it from https://github.com/tumi8/hloc. You should unzip `pages_offline.tar.gz` to get this directory. |
| admin1CodeASCII.txt | This file is used from https://www.geonames.org/, which is used to get the admin name of a city. |
| admin2CodeUK.txt    | This file is adapted from https://www.geonames.org/, which is used to get the admin name of UK city because the county is as admin 2 in Geonames but we use it for admin 1. |
| cities1000.txt      | This file is from https://www.geonames.org/, containing all cities whose population is larger than 1000. |
| clli_first6_1.csv   | This file contains the coordinate of the CLLI Code, which is from http://wedophones.com/Manuals/TelcoData/clli-lat-lon.txt |
| clli_first6_2.csv   | This file contains the corresponding city information of the CLLI Code, which is collected manually. |
| country_code.txt    | This file contains the country name and the corresponding country code, which is from https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes. |
| country_info.txt    | This file contains some information of each country, which is from https://www.geonames.org/. |
| country_region.txt  | This file contains the regional information of each country, which is from https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes. |
| country_rir.txt     | This file contains the rir information of each country, which is from https://www.nro.net/list-of-country-codes-ordered-by-rir/. |
| UNLOCODE_{1-3}.txt  | This file contains the information of UN/LOCODE, which is from https://www.nro.net/list-of-country-codes-ordered-by-rir/. |
