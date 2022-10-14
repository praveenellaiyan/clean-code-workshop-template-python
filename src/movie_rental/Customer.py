from typing import Callable

from src.movie_rental.Movie import Movie
from src.movie_rental.Rental import Rental


class Customer:
    name: str
    rentals: list[Rental]

    def __init__(self, name: str):
        self.name = name
        self.rentals = []

    def add_rental(self, rental: Rental):
        self.rentals.append(rental)

    def get_name(self) -> str:
        return self.name

    def statement(self) -> str:
        result: str = "Rental Record for " + self.get_name() + "\n"
        # show figure for this rental
        result += self.construct_statement(
            lambda rental: "\t" + rental.get_movie().get_title() + "\t" + str(self.__rental_amount(rental)) + "\n"
        )
        # add footer lines result
        result += "Amount owed is " + str(self.__total_amount()) + "\n"
        result += "You earned " + str(self.__frequent_renter_points()) + \
                  " frequent renter points"
        return result

    def __total_amount(self):
        total_amount: float = 0.0
        for each in self.rentals:
            total_amount += self.__rental_amount(each)
        return total_amount

    def __rental_amount(self, rental):
        this_amount: float = 0
        # determine amounts for each line
        if rental.get_movie().get_price_code() == Movie.REGULAR:
            this_amount += 2
            if rental.get_days_rented() > 2:
                this_amount += (rental.get_days_rented() - 2) * 1.5
        elif rental.get_movie().get_price_code() == Movie.NEW_RELEASE:
            this_amount += rental.get_days_rented() * 3
        elif rental.get_movie().get_price_code() == Movie.CHILDRENS:
            this_amount += 2
            if rental.get_days_rented() > 3:
                this_amount += (rental.get_days_rented() - 3) * 1.5
        return this_amount

    def __frequent_renter_points(self):
        frequent_renter_points: int = 0
        for each in self.rentals:
            # add frequent renter points
            frequent_renter_points += 1
            # add bonus for a two day new release rental
            if (each.get_movie().get_price_code() == Movie.NEW_RELEASE) and \
                    (each.get_days_rented() > 1):
                frequent_renter_points += 1
        return frequent_renter_points

    def construct_statement(self, formatter: Callable):
        formatted_statement = ""
        for rental in self.rentals:
            formatted_statement += formatter(rental)
        return formatted_statement

    def html_statement(self):
        return "<html><h1>Rental Record for <b>"+self.name+"</b></h1></br>" \
                + self.construct_statement(
                    lambda rental: " "+rental.movie.get_title()+" "+str(self.__rental_amount(rental))+"</br>"
                  ) + \
               "Amount owed is <b>"+str(self.__total_amount())+"</b></br>" \
               "You earned <b>"+str(self.__frequent_renter_points())+"</b> frequent renter points</html>"

