from bs4 import BeautifulSoup
from utils import write_json


def extract_body_from_html():
    print('extract_body_from_html().')

    # Opening the html file and Reading the file
    with open('apostas.html', 'r') as HTMLFile:
        file_content = HTMLFile.read()

    # Creating a BeautifulSoup object and specifying the parser
    S = BeautifulSoup(file_content, 'lxml')

    # Using the prettify method to modify the code
    with open('apostas_body.html', 'w') as HTMLFile:
        pretty = S.body.prettify()
        HTMLFile.write(pretty)


def extract_bets_from_html():
    extract_body_from_html()

    print('extract_bets_from_html().')

    # Opening the html file and Reading the file
    with open('apostas_body.html', 'r') as HTMLFile:
        file_content = HTMLFile.read()

    apostas = []

    # Creating a BeautifulSoup object and specifying the parser
    S = BeautifulSoup(file_content, 'html.parser')

    container = S.find('div', class_='mbl-BetItemsContainer_BetItemsContainer')

    contador = -1
    for elem in container:
        contador += 1
        aposta = {}

        if elem.text == '\n':
            continue

        HeaderTextContainer = elem.contents[1].contents[1]
        StakeDesc = HeaderTextContainer.contents[1]
        HeaderText = HeaderTextContainer.contents[3]
        # print(StakeDesc.text.strip(), HeaderText.text.strip())
        aposta['StakeDesc'] = StakeDesc.text.strip()
        aposta['HeaderText'] = HeaderText.text.strip()

        SubHeaderText = HeaderTextContainer.contents[5]
        # print(SubHeaderText.text.strip())
        aposta['SubHeaderText'] = SubHeaderText.text.strip()

        # print()

        InnerView = elem.contents[5]
        ParticipantContainer = InnerView.contents[1].contents[1]
        aposta['ParticipantContainer'] = []
        for BetParticipant in ParticipantContainer.contents:
            if BetParticipant.text == '\n':
                continue
            # print(BetParticipant)

            bet_participant = {}
            LeftContainer = BetParticipant.contents[1].contents[1]

            ParticipantSpan = LeftContainer.contents[1].contents[3].contents[1].contents[0]
            # print(ParticipantSpan.text.strip())
            bet_participant['ParticipantSpan'] = ParticipantSpan.text.strip()

            MarketDescription = LeftContainer.contents[3].contents[1]
            # print(MarketDescription.text.strip())
            bet_participant['MarketDescription'] = MarketDescription.text.strip()

            FixtureName = LeftContainer.contents[5].contents[1].contents[1]
            # print(FixtureName.text.strip())
            bet_participant['FixtureName'] = FixtureName.text.strip()

            FixtureStartTime = LeftContainer.contents[5].contents[1].contents[3]
            if FixtureStartTime.text != '\n':
                # print(FixtureStartTime.text.strip())
                bet_participant['FixtureStartTime'] = FixtureStartTime.text.strip()
            else:
                bet_participant['FixtureStartTime'] = ''

            HeaderOdds = BetParticipant.contents[1].contents[3]
            # print(HeaderOdds.text.strip())
            bet_participant['HeaderOdds'] = HeaderOdds.text.strip()

            # print()
            aposta['ParticipantContainer'].append(bet_participant)

        BetInformation = InnerView.contents[5].contents[1]
        StakeDisplay_Title = BetInformation.contents[1].contents[1]
        StakeDisplay_StakeWrapper = BetInformation.contents[1].contents[3]
        # print(StakeDisplay_Title.text.strip(), StakeDisplay_StakeWrapper.text.strip())
        aposta['StakeDisplay_Title'] = StakeDisplay_Title.text.strip()
        aposta['StakeDisplay_StakeWrapper'] = StakeDisplay_StakeWrapper.text.strip()

        BetInformationLabel = BetInformation.contents[3].contents[1]
        BetInformationText = BetInformation.contents[3].contents[3].contents[1]
        # print(BetInformationLabel.text.strip(), BetInformationText.text.strip())
        aposta['BetInformationLabel'] = BetInformationLabel.text.strip()
        aposta['BetInformationText'] = BetInformationText.text.strip()

        # print()
        # print('--------\n')
        apostas.append(aposta)

    apostas_dict = {
        'num_apostas': len(apostas),
        'apostas': apostas
    }
    write_json('apostas.json', apostas_dict)


if __name__ == '__main__':
    extract_bets_from_html()
