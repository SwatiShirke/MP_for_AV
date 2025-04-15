/* This file was automatically generated by CasADi 3.6.7.
 *  It consists of: 
 *   1) content generated by CasADi runtime: not copyrighted
 *   2) template code copied from CasADi source: permissively licensed (MIT-0)
 *   3) user code: owned by the user
 *
 */
#ifdef __cplusplus
extern "C" {
#endif

#ifndef casadi_real
#define casadi_real double
#endif

#ifndef casadi_int
#define casadi_int long long int
#endif

int solver(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem);
int solver_alloc_mem(void);
int solver_init_mem(int mem);
void solver_free_mem(int mem);
int solver_checkout(void);
void solver_release(int mem);
void solver_incref(void);
void solver_decref(void);
casadi_int solver_n_in(void);
casadi_int solver_n_out(void);
casadi_real solver_default_in(casadi_int i);
const char* solver_name_in(casadi_int i);
const char* solver_name_out(casadi_int i);
const casadi_int* solver_sparsity_in(casadi_int i);
const casadi_int* solver_sparsity_out(casadi_int i);
int solver_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
int solver_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w);
#define solver_SZ_ARG 12
#define solver_SZ_RES 10
#define solver_SZ_IW 0
#define solver_SZ_W 111
#ifdef __cplusplus
} /* extern "C" */
#endif
