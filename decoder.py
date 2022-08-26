from exceptions import MoreOneSignEqualError
from DecodeExpression import Decode


def decode_string(st):
	k, sign = 0, None
	for ch in st:
		if ch == "=":
			k, sign = k + 1, "="
		elif ch in ">⩾⩽<":
			k, sign = k + 1, ch
		if k > 1:
			raise MoreOneSignEqualError
	if not sign:
		return "ex", Decode().decode(st)
		#answer, obj = 
#	if sign == "=":
#		return Decoded_Equal(st).run()
#	return Decoded_Unequal(st).run()
