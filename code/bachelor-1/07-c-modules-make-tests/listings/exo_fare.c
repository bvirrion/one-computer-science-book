// exo_fare.c: the price of a bus ticket, in cents.
int fare(int age, int student)
{
    int price = 300;
    if (age < 6)
        price = 0;
    else if (age < 18 || student)
        price = 150;
    if (age >= 65)
        price = 200;
    return price;
}
