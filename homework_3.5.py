import os
import math

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
    response = requests.post(
        'http://www.webservicex.net/ConvertTemperature.asmx?WSDL',
        headers={
            'Content-Type': 'application/soap+xml; charset=utf-8',
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
              <soap12:Body>
                <ConvertTemp xmlns="http://www.webserviceX.NET/">
                  <Temperature>{}</Temperature>
                  <FromUnit>{}</FromUnit>
                  <ToUnit>{}</ToUnit>
                </ConvertTemp>
              </soap12:Body>
            </soap12:Envelope>'''.format(temperature, from_unit, to_unit)
    )
    return float(fromstring(response.text)[0][0][0].text)


def get_converted_currencies(from_unit, to_unit):
    response = requests.post(
        'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL',
        headers={
            'Content-Type': 'application/soap+xml; charset=utf-8',
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
              <soap12:Body>
                <ConversionRate xmlns="http://www.webserviceX.NET/">
                  <FromCurrency>{}</FromCurrency>
                  <ToCurrency>{}</ToCurrency>
                </ConversionRate>
              </soap12:Body>
            </soap12:Envelope>'''.format(from_unit, to_unit)
    )
    return float(fromstring(response.text)[0][0][0].text)


def get_converted_lenght(from_unit, to_unit):
    response = requests.post(
        'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL',
        headers={
            'Content-Type': 'application/soap+xml; charset=utf-8',
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
              <soap12:Body>
                <ConversionRate xmlns="http://www.webserviceX.NET/">
                  <FromCurrency>{}</FromCurrency>
                  <ToCurrency>{}</ToCurrency>
                </ConversionRate>
              </soap12:Body>
            </soap12:Envelope>'''.format(from_unit, to_unit)
    )
    return float(fromstring(response.text)[0][0][0].text)


def get_converted_kilometers(val, from_unit, to_unit):
    response = requests.post(
        'http://www.webservicex.net/length.asmx?WSDL',
        headers={
            'Content-Type': 'application/soap+xml; charset=utf-8',
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
            <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
              <soap12:Body>
                <ChangeLengthUnit xmlns="http://www.webserviceX.NET/">
                  <LengthValue>{}</LengthValue>
                  <fromLengthUnit>{}</fromLengthUnit>
                  <toLengthUnit>{}</toLengthUnit>
                </ChangeLengthUnit>
              </soap12:Body>
            </soap12:Envelope>'''.format(val, from_unit, to_unit)
    )
    return float(fromstring(response.text)[0][0][0].text)


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
