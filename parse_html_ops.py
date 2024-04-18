import os
import shutil
from bs4 import BeautifulSoup
from utils import write_json


def extract_body_from_html(main_dir: str, filename_bets_html: str, filename_betsbody_html: str):
    print('extract_body_from_html().')

    temp_dir = os.path.join(main_dir, 'temp')
    filepath_bets_html = os.path.join(main_dir, filename_bets_html)
    filepath_betsbody_html = os.path.join(temp_dir, filename_betsbody_html)

    if not os.path.exists(temp_dir):
        print('ERRO. O diretório temp não foi encontrado. será criado agora.')
        os.makedirs(temp_dir)
    else:
        print('O diretório temp já existe. será resetado agora.')
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

    # Opening the html file and Reading the file
    with open(filepath_bets_html, 'r') as HTMLFile:
        file_content = HTMLFile.read()

    # Creating a BeautifulSoup object and specifying the parser
    S = BeautifulSoup(file_content, 'lxml')

    # Using the prettify method to modify the code
    with open(filepath_betsbody_html, 'w') as HTMLFile:
        pretty = S.body.prettify()
        HTMLFile.write(pretty)


def extract_bets_from_html(main_dir: str, filename_bets_html: str, filename_betsbody_html: str, filename_bets_json: str):
    temp_dir = os.path.join(main_dir, 'temp')
    filepath_betsbody_html = os.path.join(temp_dir, filename_betsbody_html)
    filepath_bets_json = os.path.join(temp_dir, filename_bets_json)

    extract_body_from_html(main_dir, filename_bets_html, filename_betsbody_html)

    print('extract_bets_from_html().')

    # Opening the html file and Reading the file
    with open(filepath_betsbody_html, 'r') as HTMLFile:
        file_content = HTMLFile.read()

    multiple_bets = []

    # Creating a BeautifulSoup object and specifying the parser
    S = BeautifulSoup(file_content, 'html.parser')

    container = S.find('div', class_='mbl-BetItemsContainer_BetItemsContainer')

    counter = -1
    for elem in container:
        counter += 1
        multiple_bet = {}

        if elem.text == '\n':
            continue

        HeaderTextContainer = elem.contents[1].contents[1]
        StakeDesc = HeaderTextContainer.contents[1]
        HeaderText = HeaderTextContainer.contents[3]
        # print(StakeDesc.text.strip(), HeaderText.text.strip())
        multiple_bet['StakeDesc'] = StakeDesc.text.strip()
        multiple_bet['HeaderText'] = HeaderText.text.strip()

        SubHeaderText = HeaderTextContainer.contents[5]
        # print(SubHeaderText.text.strip())
        multiple_bet['SubHeaderText'] = SubHeaderText.text.strip()

        # print()

        InnerView = elem.contents[5]
        ParticipantContainer = InnerView.contents[1].contents[1]
        multiple_bet['ParticipantContainer'] = []
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
            multiple_bet['ParticipantContainer'].append(bet_participant)

        BetInformation = InnerView.contents[5].contents[1]
        StakeDisplay_Title = BetInformation.contents[1].contents[1]
        StakeDisplay_StakeWrapper = BetInformation.contents[1].contents[3]
        # print(StakeDisplay_Title.text.strip(), StakeDisplay_StakeWrapper.text.strip())
        multiple_bet['StakeDisplay_Title'] = StakeDisplay_Title.text.strip()
        multiple_bet['StakeDisplay_StakeWrapper'] = StakeDisplay_StakeWrapper.text.strip()

        BetInformationLabel = BetInformation.contents[3].contents[1]
        BetInformationText = BetInformation.contents[3].contents[3].contents[1]
        # print(BetInformationLabel.text.strip(), BetInformationText.text.strip())
        multiple_bet['BetInformationLabel'] = BetInformationLabel.text.strip()
        multiple_bet['BetInformationText'] = BetInformationText.text.strip()

        # print()
        # print('--------\n')
        multiple_bets.append(multiple_bet)

    multiple_bets_dict = {
        'n_bets': len(multiple_bets),
        'bets': multiple_bets
    }
    write_json(filepath_bets_json, multiple_bets_dict)


if __name__ == '__main__':
    cur_dir = os.curdir

    extract_bets_from_html(cur_dir, 'bets.html', 'bets_body.html', 'bets.json')
