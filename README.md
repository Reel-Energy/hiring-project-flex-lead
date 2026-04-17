# Case for the technical interview of the Flexibility Trading Lead position

This is a coding exercise for the position of [Flexibility Trading Lead](https://reelenergy-1727862339.teamtailor.com/jobs/7492540-flexibility-trading-lead) at Reel.
Please fork this repository and share your solved exercise to es@reel.energy Cc di@reel.energy, msl@reel.energy.

We will discuss your solution (and any other ideas you did not have time to build for this exercise) in the interview. Please do not use more than three hours on this. If in doubt, prioritize business logic over code quality. Feel free to use AI as a help but be prepared to answer questions about choices made in your code and solution.

If you think the exercise is ignoring very important details, feel free to deviate from the exact assignment but be prepared to justify your choices.

### Introduction
Reel has a sizeable portfolio of hybrid plants with co-located solar PV and storage. Our job is to maximize the earnings for these plants through optimal multi-market participation.

## The task
Devise a trading strategy for a 100 MW PV + 50 MW / 200 MWh BESS site with a 95 MW grid connection (both import and export to and from the grid are possible) located in DK1.
The asset should participate in the aFRR capacity market and in the day-ahead auction.
Your code has to output two results:
- a price/volume matrix with the bids for participating in aFRR capacity;
- a price/volume matrix with the bids for buying and selling in the day-ahead auction, after the results of the aFRR capacity auction are known.

Sign convention is positive for selling energy in the day-ahead auction (note: this is contrary to what is actually implemented at the exchange but we keep it like this to avoid confusion in this exercise). 
Sign convention for aFRR capacity is positive for up-regulation, negative for down-regulation.
We provide an example of the bid matrix structure for day-ahead in `/helpers/bids.py`.

### The markets
#### aFRR capacity
The aFRR capacity market is designed to ensure that a specific volume of upward and downward flexibility is reserved 24 hours in advance and available for real-time activation.
In practice Energinet imposes constraints for limited energy reservoir units (LERs) that limit the maximum amount of capacity to be bid. Please ignore those constraints, but keep in mind that if you bid capacity at day-ahead, then you MUST have it available in delivery at all costs.

- Market Time Unit (MTU): The market operates with 1-hour granularity, meaning that each hour is cleared independently.
- Bid Increments: The minimum bid size is 1 MW, with a granularity of 1 MW. One can post multiple price/volume pairs in a bid for the same period
- Directionality: aFRR is procured as separate upward and downward products, allowing participants to bid for one direction or both (asymmetric bidding).
- Gate closure: 07:30 CET
  
More information available [here](https://nordicbalancingmodel.net/wp-content/uploads/2024/12/Market-handbook-FRR-CM-Version-2.0.pdf).

#### Day-ahead
The day-ahead auction is the main market for electricity with plenty of liquidity.
- Market Time Unit (MTU): 15min
- Gate closure: 12:00 CET
- Granularity: 0.1 MW

### Assumptions
General:
- perfect foresight of spot prices for day ahead
- no distribution and grid tariffs
  
BESS:
- 100% round-trip efficiency
- limited to 2 cycles/day. One cycle is defined as discharged energy over a given period divided by energy capacity.
- cost per cycle of 25 EUR/MWh. We want to (ideally) only cycle if we can make a profit larger than that. Note that this is not a cash cost, but rather a depreciation of the battery due to degradation.

PV:
- assume perfect foresight of generation for day ahead
- assume control is in place and the asset setpoint can be changed to any value between 0-95 MW with no ramping constraints

### Data
You can use any publicly available dataset of your choice to make your case more realistic. Here we suggest a few data sources, but feel free to use other ones.
For the sources listed below, we provide helper functions in `/helpers/data.py`.
- [Solar forecasts](https://www.energidataservice.dk/tso-electricity/Forecasts_5Min): make sure to scale them such that they could realistically represent a PV asset of the characteristics described above
- [Day-ahead prices](https://www.energidataservice.dk/tso-electricity/DayAheadPrices)
- [Capacity market data](https://www.energidataservice.dk/tso-electricity/AfrrReservesNordic)
