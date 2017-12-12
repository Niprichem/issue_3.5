import os
import math

import osa
import requests
from xml.etree.ElementTree import fromstring


def get_temperature_from_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield float(line.strip().replace(' F', ''))


def get_currency_from_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            _, val, currency = line.strip().split(' ')
            yield float(val), currency


def get_miles_from_file(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            yield float(line.strip().split(' ')[1].replace(',', ''))


def get_converted_temperature(temperature, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    return client.service.ConvertTemp(Temperature=temperature, FromUnit=from_unit, ToUnit=to_unit)


def get_converted_currencies(from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/CurrencyConvertor.asmx?WSDL')
    return client.service.ConversionRate(FromCurrency=from_unit, ToCurrency=to_unit)


def get_converted_kilometers(val, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    return client.service.ChangeLengthUnit(LengthValue=val, fromLengthUnit=from_unit, toLengthUnit=to_unit)


def main():
    source = 'source'
    temerature_file_name = 'temps.txt'
    currency_file_name = 'currencies.txt'
    travel_file_name = 'travel.txt'
    temperature = 0
    i = 0.
    for t in get_temperature_from_file(os.path.join(source, temerature_file_name)):
        i += 1.
        temperature += get_converted_temperature(t, 'degreeFahrenheit', 'degreeCelsius')
    print('Средняя температура:', temperature/i, 'С')

    money = 0
    for val, from_unit in get_currency_from_file(os.path.join(source, currency_file_name)):
        money += math.ceil(val*get_converted_currencies(from_unit, 'RUB'))
    print('Потрачено на путешествие:', money, 'руб')

    length = 0
    for val in get_miles_from_file(os.path.join(source, travel_file_name)):
        length += get_converted_kilometers(val, 'Miles', 'Kilometers')
    print('Суммарный путь:', round(length, 2), 'км')


if __name__ == '__main__':
    main()
