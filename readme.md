**TODO:** 
- [ ] Change file system shared storage for sharing information to a socket communication system.

- [ ] Middle ware will return report, if possible, as graphics.
- [ ] Possibly with means of each report.

Inv. ***Encadenacion cliente-servidor con C.***

Convert traces to the number of workers, ie, n traces.

Divide interarrivals in n of workers using round robin, ie. first instance of trace to server 1, 
second to server 2, third to server 3, foruht to 1 again and on and on.

Separate those and get the mean of each array, ie, if the traces for server 1 where selected like [1, 3, 7], 
ie the first arrived in 1, the second in 3, the third in 7, etc, get differences [3 - 1 = 2, 7 - 3 = 4],
sum and get mean, mean = 3. Techinically each worker should have the same or similar arrival time average(mean)
But that is a s"simulated" time, so the values on the array are not going to be lineal.

In order to simplify the process, the static service time, 
Service time should be: 
- logarithmic, use the values shown in the test table on the xlsx file.
