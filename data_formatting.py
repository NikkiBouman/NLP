import pandas as pd
import torch
from Language import Language, normalizeString, MRLanguage, normalizeMRString

pd.set_option('display.max_colwidth', None)


def indexesFromSentence(lang, sentence, delimeter=' '):
    indices = [lang.word2index[word] for word in sentence.split(delimeter)]
    return torch.tensor(indices)


def get_output_data(file):
    corpus_df = pd.read_csv(file)
    lang_df = corpus_df['ref']

    natural_lang = Language()
    natural_lang.readLang(lang_df)
    corpus_df['ref'] = corpus_df['ref'].astype(str) + ' eos'
    corpus_df['ref'] = corpus_df['ref'].apply(lambda x: normalizeString(x))
    corpus_df['ref'] = corpus_df['ref'].apply(lambda x: indexesFromSentence(natural_lang, x))

    return corpus_df['ref'], natural_lang

def get_input_data(file):
    corpus_df = pd.read_csv(file)
    lang_df = corpus_df['mr']

    mr_lang = MRLanguage()
    mr_lang.readLang(corpus_df['mr'])
    corpus_df['mr'] = corpus_df['mr'].astype(str) + ', eos'
    corpus_df['mr'] = corpus_df['mr'].apply(lambda x: normalizeMRString(x))
    corpus_df['mr'] = corpus_df['mr'].apply(lambda x: indexesFromSentence(mr_lang, x, delimeter=", "))

    return corpus_df['mr'], mr_lang






#
# def tensorFromSentence(lang, sentence):
#     indexes = indexesFromSentence(lang, sentence)
#     indexes.append(EOS_token)
#     return torch.tensor(indexes, dtype=torch.long, device=device).view(-1, 1)
#
# def tensorsFromPair(pair):
#     input_tensor = tensorFromSentence(input_lang, pair[0])
#     target_tensor = tensorFromSentence(output_lang, pair[1])
#     return (input_tensor, target_tensor)

# teacher_forcing_ratio = 0.5
# MAX_LENGTH = 80
#
#
# def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion, max_length=MAX_LENGTH):
#     encoder_hidden = encoder.initHidden()
#
#     encoder_optimizer.zero_grad()
#     decoder_optimizer.zero_grad()
#
#     input_length = input_tensor.size(0)
#     target_length = target_tensor.size(0)
#
#     encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=device)
#
#     loss = 0
#
#     for ei in range(input_length):
#         encoder_output, encoder_hidden = encoder(
#             input_tensor[ei], encoder_hidden)
#         encoder_outputs[ei] = encoder_output[0, 0]
#
#     decoder_input = torch.tensor([[SOS_token]], device=device)
#
#     decoder_hidden = encoder_hidden
#
#     use_teacher_forcing = True if random.random() < teacher_forcing_ratio else False
#
#     if use_teacher_forcing:
#         # Teacher forcing: Feed the target as the next input
#         for di in range(target_length):
#             decoder_output, decoder_hidden, decoder_attention = decoder(
#                 decoder_input, decoder_hidden, encoder_outputs)
#             loss += criterion(decoder_output, target_tensor[di])
#             decoder_input = target_tensor[di]  # Teacher forcing
#
#     else:
#         # Without teacher forcing: use its own predictions as the next input
#         for di in range(target_length):
#             decoder_output, decoder_hidden, decoder_attention = decoder(
#                 decoder_input, decoder_hidden, encoder_outputs)
#             topv, topi = decoder_output.topk(1)
#             decoder_input = topi.squeeze().detach()  # detach from history as input
#
#             loss += criterion(decoder_output, target_tensor[di])
#             if decoder_input.item() == EOS_token:
#                 break
#
#     loss.backward()
#
#     encoder_optimizer.step()
#     decoder_optimizer.step()
#
#     return loss.item() / target_length
