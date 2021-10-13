#define PRNT_RATE					1		// Rate at which to report data
#define PRNT_DATA                   1       // Report pop data while running
#define PRNT_STAT					1		// Report pop stats 
#define PRNT_CHRS					0		// Report raw chromosome data
#define PRNT_INFO					1		// Report human-readable data
#define PRNT_FITS					1		// Report individual fitness
#define BUFFER_SIZE					64

#define CROSSOVER_RATE				0.8
#define MUTATION_RATE				0.005

//#define MUTATION_RATE				0.05

#define FF_SIMPLE					0
#define FF_SHPATH					1
#define M_FIXED_GENERATIONS			0
#define M_MAX_FITNESS_THRESHHOLD	1
#define M_AVG_FITNESS_THRESHHOLD	2
#define M_LOCAL_CONVERGENCE			3

#define DEFAULT_RAND_SEED			42
#define DEFAULT_FF_TYPE				FF_SIMPLE
#define DEFAULT_END_TYPE			M_FIXED_GENERATIONS
//#define DEFAULT_POP_SIZE			4
#define DEFAULT_END_GENERATION		20
#define DEFAULT_F_THRESH_SIMPLE		125000.0
#define DEFAULT_F_THRESH_SHPATH		10000.0
#define DEFAULT_CONV_GENS			20
#define DEFAULT_CONV_VARIATION		100

//#define CHR_SIZE_SIMPLE				12

#define SP_BOUND					2048
#define N_POINTS					32
#define COORD_SIZE					12
#define CHR_SIZE_SHPATH				COORD_SIZE*3*N_POINTS
#define COLLISION_COST				100

/****************** SQX ADD *************************/
#define MAX_COST 1000000000
//#define FUNC_NUM 15
#define DEFAULT_POP_SIZE			16
//#define DEFAULT_POP_SIZE			16
#define DIM 1
#define SEARCH_RANGE 14
#define CHR_SIZE_SIMPLE				DIM*SEARCH_RANGE
//#define NOT_SINGLE_IERATION


