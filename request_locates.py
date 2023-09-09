import csv
import random


def read_request_from_csv(filename: str) -> list[dict]:
    client_requests = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            entry = {headers[i]: row[i] for i in range(len(headers))}
            client_requests.append(entry)
    return client_requests


def write_approved_request_to_csv(data_list: list, filename: str) -> None:
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_list[0].keys())
        writer.writeheader()
        for row in data_list:
            writer.writerow(row)


def aggregate_requests_by_symbol(client_requests: list) -> dict:
    """
    aggregates all requests per symbol
    :param client_requests: list of requests that include requested symbol and number_of_locates_requested
    :return: dict[str, int] of symbols and total of number_of_locates_requested per symbol
    """
    symbol_request_dict = {}
    for client_request in client_requests:
        if client_request['symbol'] in symbol_request_dict:
            symbol_request_dict[client_request['symbol']] += int(client_request['number_of_locates_requested'])
        else:
            symbol_request_dict[client_request['symbol']] = int(client_request['number_of_locates_requested'])
    return symbol_request_dict


def request_locates(requested_locates: dict[str, int]) -> dict[str, int]:
    """
    Generates random request answer
    :param requested_locates: dict of symbols with number of locates requested
    :return: dict of symbols with approved number of locates
    """
    approved_locates = {}
    for symbol, request_num in requested_locates.items():
        if random.choice([True, False]):
            approval_rate = random.uniform(0.5, 1.0)  # Randomly select a rate between 0.5 and 1
            approved_locates[symbol] = int(request_num * approval_rate)
    return approved_locates


def distribute_locates(client_requests: list[dict],
                       requested_locates: dict[str, int],
                       approved_locates: dict[str, int]) -> None:
    """
    Distributes the approved locates and update client requests based on the following logic:
    - approval by proportion to request
    - round up to 100 if possible
    :param client_requests: list of client requests by symbol and number of locates
    :param requested_locates: dict of requested locates by symbol
    :param approved_locates: dict of approved locates by symbol
    """
    for client_request in client_requests:
        symbol = client_request['symbol']
        total_approved_for_symbol = approved_locates.get(symbol)
        if total_approved_for_symbol:
            client_requested = int(client_request['number_of_locates_requested'])
            percent_of_total_request = client_requested / requested_locates[symbol]
            if percent_of_total_request == 1:
                client_approved = total_approved_for_symbol
            else:
                client_approved = min(round(total_approved_for_symbol * percent_of_total_request / 100) * 100,
                                      total_approved_for_symbol)
                requested_locates[symbol] -= client_requested
                approved_locates[symbol] -= client_approved
        else:
            client_approved = 0
        client_request['number_of_locates_approved'] = client_approved
        client_request.pop('number_of_locates_requested')


# Read all requests from the CSV file.
client_requests = read_request_from_csv(filename='client_requests.csv')

# Aggregate all the requests for each symbol.
requests_by_symbol = aggregate_requests_by_symbol(client_requests=client_requests)

# Call request_locates with the aggregated result.
approved_requests = request_locates(requested_locates=requests_by_symbol)

# Distribute the result to the clients.
distribute_locates(client_requests=client_requests,
                   requested_locates=requests_by_symbol,
                   approved_locates=approved_requests)

# write results to CSV file
write_approved_request_to_csv(data_list=client_requests, filename='approved_requests.csv')
