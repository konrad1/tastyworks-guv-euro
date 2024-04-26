Tastyworks GuV Euro
-------------------

Create a PnL-document for a tax income statement in Germany for the US-broker tastyworks.
Download tax dodument of gains losses from Tastyworks into a csv file ("YYYY-<Account-nr>-gain-loss.csv") and create with this
python-script a new enhanced csv-file. This new csv-file adds a currency conversion
from USD to Euro of column NO_WS_GAINLOSS.
Translate Header of csv to german.
No tax advice

requirements
------------
python library pandas
csv of euro exchange rates from bundesbank.de: https://www.bundesbank.de/statistic-rmi/StatisticDownload?tsId=BBEX3.D.USD.EUR.BB.AC.000&its_csvFormat=en&its_fileFormat=csv&mode=its&its_from=2010
