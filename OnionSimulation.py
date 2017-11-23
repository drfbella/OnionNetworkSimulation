import re
import time

import rsa
from rsa.bigfile import *

def onion_encrypt(message, path, keys):
  """
  Encrypts a message using a sequence of public keys representing the keys on
  the onion path between the two end systems.
  """
  print("\nPHASE 2: ENCRYPTING THE MESSAGE (message={}) USING THE PUBLIC KEYS OF THE {} RELAYS ALONG THE PATH.\n".format(message, len(path)-1))

  print("Original message: {}".format(message), end="\n")

  message_bytes = message.encode("utf8")

  print("Original payload size: {} bytes.\n".format(len(message_bytes)))

  path = path[::-1]

  for node in path[:-1]:
    print("Encrypting for {}'s public key.".format(node))

    with open("infile.txt", "wb") as outf:
      outf.write(message_bytes)

    local_start = time.time()
    with open('infile.txt', 'rb') as infile, open('outfile.txt', 'wb') as outfile:
      encrypt_bigfile(infile, outfile, keys[node][0])
    local_end = time.time()

    print("Encryption time: {}ms\n".format((local_end-local_start) * 1000.0))

    with open("outfile.txt", "rb") as inf:
      message_bytes = inf.read()

    print("Payload size now {} bytes".format(len(message_bytes)))

  return message_bytes


def onion_decrypt(message, priv_key):
  """
  Removes a layer of encryption from the message.
  """
  with open("infile.txt", "wb") as outf:
    outf.write(message)

  local_start = time.time()
  with open('infile.txt', 'rb') as infile, open('outfile.txt', 'wb') as outfile:
    decrypt_bigfile(infile, outfile, priv_key)
  local_end = time.time()

  print("Decryption time: {}ms\n".format((local_end-local_start) * 1000.0))

  with open("outfile.txt", "rb") as inf:
    message = inf.read()

  return message

def onion_send(message, path):
  """
  Sends a message through the network.
  """
  end_systems = [node for node in path if re.match("[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*\.[1-9][0-9]*", node)]

  keys = onion_make_keys(end_systems)

  encrypted_message = onion_encrypt(message, end_systems, keys)
  
  print("\nPHASE 3: BOUNCING THE MESSAGE ALONG THE PATH ({} NODES, {} RELAYS)\n".format(len(path)-2, len(end_systems)-2))

  print("Message sent from {}".format(path[0]))

  for node in path[1:]:
    print("Message hopped to {}".format(node))

    if node in end_systems:
      print("Decrypting using {}'s private key.".format(node))
      encrypted_message = onion_decrypt(encrypted_message, keys[node][1])

  print("\nMessage arrived at destination: \"{}\".\n".format(encrypted_message.decode("utf8")))


def onion_make_keys(path):
  """
  Generates keys for the nodes in the path.
  """
  print("\nPHASE 1: GENERATING KEYS FOR THE RELAYS ON THE PATH.", end="\n")

  keys = dict()

  for node in path[1:]:
    print("Generating key pair for {}".format(node))
    local_start = time.time()
    keys[node] = rsa.newkeys(1024)
    local_end = time.time()
    print("Key pair generated for {} (TIME: {}ms)".format(node, (local_end - local_start) * 1000.0))

  return keys