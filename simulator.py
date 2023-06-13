import numpy as np
import pandas as pd
from datetime import datetime, timedelta

transition_matrix = pd.read_csv("./output/transition_matrix.csv", index_col = 0)
states = ["checkout", "dairy", "drinks", "fruit", "spices"]

class Customer():
    """
    A single customer that moves through the supermarket.
    """

    def __init__(self, state = "entrance", active = True):
        self.state = state
        self.transition_matrix = transition_matrix

    def next_state(self):
        """
        Propagates the customer to the next state per the transition matrix probabilities, returns nothing.
        """

        self.state = np.random.choice(states, p = self.transition_matrix.loc[self.state].values)

class Supermarket():
    """
    Manages multiple customer instances currently in the market, adds a new one every minute, and removes them once they reach the checkout. Simulated customer activity is written to a dataframe which is then written to a .csv file.
    """

    def __init__(self, start_time = "07:00", end_time = "22:00"):
        """
        Initializes instance with start and end times in HH:MM formats.
        """
        start_time = datetime.strptime(start_time, "%H:%M")
        end_time = datetime.strptime(end_time, "%H:%M")

        self.start_time = start_time
        self.end_time = end_time
        self.time = start_time
        self.minutes_open = (self.end_time - self.start_time).total_seconds() / 60
        self.minutes_open = int(self.minutes_open)

        self.customers = []

        self.simulation_track = pd.DataFrame(columns = ["customer_id", "timestamp", "location"])

    def run(self):
        """
        Opens the supermarket, adds new customers, moves them every minute, and writes their activity to a dataframe. Once the end time is reached, the dataframe is saved as a .csv file for further processing.
        """

        while self.time <= self.end_time:
            self.add_new_customer()
            self.supermarket_status() # not strictly necessary, but useful for future development

            for customer in self.customers:
                self.simulation_track = pd.concat([self.simulation_track, pd.DataFrame([[customer, str(self.time.time())[0:5], customer.state]], columns = self.simulation_track.columns)], ignore_index = True)
            
            self.next_minute()
            self.time = self.time + timedelta(minutes = 1)
            
        self.simulation_track.to_csv(f"./output/simulation_{datetime.now().strftime('%Y%m%d%H%M')}.csv")

    def next_minute(self):
        """
        Moves all customers 1 minute forward in time, removes those that have reached the checkout.
        """

        for customer in self.customers:
            customer.next_state()

            if customer.state == "checkout":
                self.customers.remove(customer)

    def supermarket_status(self):
        """
        Prints the time and how many customers are located where in the supermarket.
        """

        print(str(self.time.time())[0:5], len(self.customers), "customers in-store")

    def add_new_customer(self):
        """
        Creates a new customer at the entrance
        """

        new_customer = Customer()
        self.customers.append(new_customer)

market = Supermarket()
market.run()