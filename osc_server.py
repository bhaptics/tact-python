import argparse
import math
from bhaptics import haptic_player;

from pythonosc import dispatcher
from pythonosc import osc_server

player = haptic_player.HapticPlayer()


def handle_front(unused_addr, args):
  print("front {0}".format(args))
  res = args.split(',')
  player.submit_dot('back', 'VestFront', [{"index": res[0], "intensity": res[1]}], 100)


def handle_back(unused_addr, args):
  print("back: {0}".format(args))
  res = args.split(',')
  player.submit_dot('back', 'VestBack', [{"index": res[0], "intensity": res[1]}], 100)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/vest_front", handle_front)
  dispatcher.map("/vest_back", handle_back)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))


  server.serve_forever()