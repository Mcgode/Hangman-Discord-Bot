from HangmanSolve import HangmanSolve


class HangmanLogic:

    # "Idle", "Figuring out", "Completing", "Failed"
    current_status = ""
    last_letter = ""
    letters_to_be_used = []
    current_solving = HangmanSolve(0)
    number_of_remaining_games = 0
    learn = False
    force_completing = False

    def __init__(self, attempts):
        self.current_status = "Idle"
        self.number_of_remaining_games = attempts

    async def call(self, client, message):

        embed = message.embeds[0]
        title = ""
        if 'title' in embed:
            title = embed['title']

        if title == "Hangman game started":
            print("Will start figuring out")
            self.current_status = "Figuring out"
            txt = embed['description'].split('\n')[0].replace('`', '').replace('-', '')\
                .replace(':', '').replace('\u2000', '').replace(' ', '').replace('.', '')
            self.current_solving = HangmanSolve(len(txt))
            self.last_letter = self.current_solving.next_discriminative_letter()
            await client.send_message(message.channel, self.last_letter)
            self.number_of_remaining_games -= 1

        elif title == "Hangman Game":
            if "Game ended" in embed['description']:
                # print(embed['description'])
                if self.learn and "You **LOSE**" in embed['description']:
                    txt = embed['fields'][0]['value']
                    # print(embed)
                    print(txt)
                    with open('./List.txt', 'a') as f:
                        f.write('\n{0}'.format(txt))
                await self.go_idle(client, message)

            elif self.current_status == "Figuring out":
                txt = embed['description'].split('\n')[1].replace('`', '')
                txt = txt.replace('-', '').replace(':', '').replace('.', '')
                txt = txt.replace('\u2000', '').replace(' ', '')
                self.current_solving.parse_input(txt, self.last_letter)
                if len(self.current_solving.selection) == 0:
                    self.current_status = "Failed"
                    await self.call(client, message)
                elif len(self.current_solving.selection) == 1:
                    self.current_status = "Completing"
                    i = 0
                    self.letters_to_be_used = []
                    word = self.current_solving.selection[0].replace(' ', '').replace('-', '').replace('.', '')
                    while i < len(word):
                        if word[i] not in self.current_solving.used_letters and word[i] not in self.letters_to_be_used:
                            self.current_solving.used_letters.append(word[i])
                            self.letters_to_be_used.append(word[i])
                        i += 1
                    print("{0} letters to be used: {1}".format(len(self.letters_to_be_used), self.letters_to_be_used))
                    self.current_solving.selection = []
                    self.force_completing = True
                    await self.call(client, message)
                else:
                    self.last_letter = self.current_solving.next_discriminative_letter()
                    await client.send_message(message.channel, self.last_letter)

            elif self.current_status == "Completing":
                if 'does not exist' in embed['description'] and not self.force_completing:
                    self.current_status = "Failed"
                    await self.call(client, message)
                elif len(self.letters_to_be_used):
                    self.force_completing = False
                    message_to_send = self.letters_to_be_used.pop()
                    print('Message to be sent for completing: {0}'.format(message_to_send))
                    await client.send_message(message.channel, message_to_send)

            elif self.current_status == "Failed":
                if self.learn:
                    await client.send_message(message.channel, 'a')
                else:
                    await client.send_message(message.channel, '.hangmanstop')
                    await self.go_idle(client, message)

    async def go_idle(self, client, message):
        self.current_status = "Idle"
        if self.number_of_remaining_games > 0:
            await client.send_message(message.channel, '.hangman Countries')


