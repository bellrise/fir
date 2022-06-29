/* Definitions for the Fir Protocol.
   Copyright (c) 2022 bellrise */

#ifndef FIR_H
#define FIR_H

#include <stdint.h>


/* packed struct attribute */
#if !defined(_fir_packed_)
# if !defined(__GNUC__) && !defined(__clang__) && !defined(__chibicc__)
#  error "No compiler supporting __attribute__((packed))"
# endif
# define _fir_packed_   __attribute__((packed))
#endif


/* The Fir Protocol listens on this port, so other devices can check the network
   for this port open, and then ask for a ACK packet. */
#define FIR_PORT        7708


/* The packet header size in bytes should be exactly this value. */
#define FIR_HEADER_SIZE 16


/* Fir packet version. The f_ver field in the packet header is set to this
   value, so other devices know whether the asking device is using the proper
   protocol version. */
#define FIR_PROT_VER    1


enum fir_packet_type
{
	FIR_PING,       /* ping */
	FIR_ERR,        /* packet containing an error message */
	FIR_RAW,        /* raw bytes */
};


enum fir_payload_type
{
	/* Raw bytes - f_size bytes after the packet header. */
	FIR_PAYLOAD_RAW,
};


struct _fir_packed_ fir_packet_header
{
	uint16_t f_ver;                 /* FIR_PROT_VER */
	uint16_t f_type;                /* one of fir_packet_type */
	uint16_t f_time;                /* time sent */
	uint16_t f_size;                /* payload size */
	uint8_t  f_ptype;               /* one of fir_payload_type */
	uint8_t  f__0[7];
};


#endif /* FIR_H */
