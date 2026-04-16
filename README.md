# Case for the technical interview of the Flexibility Trading Lead position

This is a coding exercise for the position of [Flexibility Trading Lead](https://reelenergy-1727862339.teamtailor.com/jobs/7492540-flexibility-trading-lead) at Reel.
Please fork this repository and share your solved exercise to es@reel.energy and di@reel.energy.

## Introduction
Reel has a sizeable portfolio of hybrid plants with co-located solar PV and storage. Our job is to maximize the earnings for these plants through optimal multi-market participation.

## The task
Devise a trading strategy for a 100 MW PV + 50 MW / 100 MWh BESS site with a 95 MW grid connection (both import and export to and from the grid are possible) located in DK1.
The asset should participate in the aFRR capacity market and in the day-ahead auction.
Your code has to output two results:
- a price/volume matrix with the bids for participating in aFRR capacity
- a price/volume matrix with the bids for buying and selling in the day-ahead auction

### The markets
#### aFRR capacity
The aFRR capacity market is designed to ensure that a specific volume of upward and downward flexibility is reserved 24 hours in advance and available for real-time activation.

- Market Time Unit (MTU): The market operates with 1-hour granularity, meaning that each hour is cleared independently. It is possible to link 
- Bid Increments: The minimum bid size is 1 MW, with a granularity of 1 MW. One can post multiple price/volume pairs in a bid for the same period
- Directionality: aFRR is procured as separate upward and downward products, allowing participants to bid for one direction or both (asymmetric bidding).
- Gate closure: 07:30 CET
  
More information available [here](https://nordicbalancingmodel.net/wp-content/uploads/2024/12/Market-handbook-FRR-CM-Version-2.0.pdf)

#### Day-ahead
The day-ahead auction is the main market for electricity with plenty of liquidity.
- Market Time Unit (MTU): 15min
- Gate closure: 12:00 CET
- Granularity: 0.1 MW

### Assumptions
Trading:
- perfect foresight of spot prices 1 day ahead
BESS:
- 100% round-trip efficiency
- limited to 2 cycles/day. One cycle is defined as discharged energy over a given period divided by energy capacity.
PV:
- assume perfect foresight of generation
- assume control is in place and the asset setpoint can be changed to any value between 0-95 MW with no ramping constraints

### Data
You can use any publicly available dataset of your choice to make your case more realistic. Here we suggest a few data sources, but feel free to use other ones.
- [Solar forecasts](Energinethttps://www.energidataservice.dk/tso-electricity/Forecasts_5Min): make sure to scale them such that they could realistically represent a PV asset of the characteristics described above
- [Day-ahead prices](https://www.energidataservice.dk/tso-electricity/DayAheadPrices)
