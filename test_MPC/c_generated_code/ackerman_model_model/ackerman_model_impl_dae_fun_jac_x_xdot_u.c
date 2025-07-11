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

/* How to prefix internal symbols */
#ifdef CASADI_CODEGEN_PREFIX
  #define CASADI_NAMESPACE_CONCAT(NS, ID) _CASADI_NAMESPACE_CONCAT(NS, ID)
  #define _CASADI_NAMESPACE_CONCAT(NS, ID) NS ## ID
  #define CASADI_PREFIX(ID) CASADI_NAMESPACE_CONCAT(CODEGEN_PREFIX, ID)
#else
  #define CASADI_PREFIX(ID) ackerman_model_impl_dae_fun_jac_x_xdot_u_ ## ID
#endif

#include <math.h>

#ifndef casadi_real
#define casadi_real double
#endif

#ifndef casadi_int
#define casadi_int int
#endif

/* Add prefix to internal symbols */
#define casadi_f0 CASADI_PREFIX(f0)
#define casadi_s0 CASADI_PREFIX(s0)
#define casadi_s1 CASADI_PREFIX(s1)
#define casadi_s2 CASADI_PREFIX(s2)
#define casadi_s3 CASADI_PREFIX(s3)
#define casadi_s4 CASADI_PREFIX(s4)
#define casadi_s5 CASADI_PREFIX(s5)
#define casadi_s6 CASADI_PREFIX(s6)
#define casadi_sq CASADI_PREFIX(sq)

/* Symbol visibility in DLLs */
#ifndef CASADI_SYMBOL_EXPORT
  #if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
    #if defined(STATIC_LINKED)
      #define CASADI_SYMBOL_EXPORT
    #else
      #define CASADI_SYMBOL_EXPORT __declspec(dllexport)
    #endif
  #elif defined(__GNUC__) && defined(GCC_HASCLASSVISIBILITY)
    #define CASADI_SYMBOL_EXPORT __attribute__ ((visibility ("default")))
  #else
    #define CASADI_SYMBOL_EXPORT
  #endif
#endif

casadi_real casadi_sq(casadi_real x) { return x*x;}

static const casadi_int casadi_s0[8] = {4, 1, 0, 4, 0, 1, 2, 3};
static const casadi_int casadi_s1[48] = {44, 1, 0, 44, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43};
static const casadi_int casadi_s2[3] = {0, 0, 0};
static const casadi_int casadi_s3[84] = {80, 1, 0, 80, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79};
static const casadi_int casadi_s4[9] = {4, 4, 0, 0, 0, 2, 2, 0, 1};
static const casadi_int casadi_s5[11] = {4, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3};
static const casadi_int casadi_s6[53] = {4, 44, 0, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 1, 2, 3, 2, 2};

/* ackerman_model_impl_dae_fun_jac_x_xdot_u:(i0[4],i1[4],i2[44],i3[],i4[],i5[80])->(o0[4],o1[4x4,2nz],o2[4x4,4nz],o3[4x44,6nz]) */
static int casadi_f0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem) {
  casadi_real a0, a1, a2, a3, a4, a5, a6, a7, a8;
  a0=arg[1]? arg[1][0] : 0;
  a1=arg[2]? arg[2][0] : 0;
  a2=arg[0]? arg[0][2] : 0;
  a3=cos(a2);
  a4=(a1*a3);
  a0=(a0-a4);
  if (res[0]!=0) res[0][0]=a0;
  a0=arg[1]? arg[1][1] : 0;
  a4=sin(a2);
  a5=(a1*a4);
  a0=(a0-a5);
  if (res[0]!=0) res[0][1]=a0;
  a0=arg[1]? arg[1][2] : 0;
  a5=2.;
  a6=(a1/a5);
  a7=arg[2]? arg[2][1] : 0;
  a8=arg[2]? arg[2][2] : 0;
  a7=(a7+a8);
  a7=(a7/a5);
  a5=tan(a7);
  a8=(a6*a5);
  a0=(a0-a8);
  if (res[0]!=0) res[0][2]=a0;
  a0=arg[1]? arg[1][3] : 0;
  a0=(a0-a1);
  if (res[0]!=0) res[0][3]=a0;
  a0=sin(a2);
  a0=(a1*a0);
  if (res[1]!=0) res[1][0]=a0;
  a2=cos(a2);
  a1=(a1*a2);
  a1=(-a1);
  if (res[1]!=0) res[1][1]=a1;
  a1=1.;
  if (res[2]!=0) res[2][0]=a1;
  if (res[2]!=0) res[2][1]=a1;
  if (res[2]!=0) res[2][2]=a1;
  if (res[2]!=0) res[2][3]=a1;
  a3=(-a3);
  if (res[3]!=0) res[3][0]=a3;
  a4=(-a4);
  if (res[3]!=0) res[3][1]=a4;
  a4=5.0000000000000000e-01;
  a5=(a4*a5);
  a5=(-a5);
  if (res[3]!=0) res[3][2]=a5;
  a5=-1.;
  if (res[3]!=0) res[3][3]=a5;
  a7=cos(a7);
  a7=casadi_sq(a7);
  a5=(a4/a7);
  a5=(a6*a5);
  a5=(-a5);
  if (res[3]!=0) res[3][4]=a5;
  a4=(a4/a7);
  a6=(a6*a4);
  a6=(-a6);
  if (res[3]!=0) res[3][5]=a6;
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem){
  return casadi_f0(arg, res, iw, w, mem);
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u_alloc_mem(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u_init_mem(int mem) {
  return 0;
}

CASADI_SYMBOL_EXPORT void ackerman_model_impl_dae_fun_jac_x_xdot_u_free_mem(int mem) {
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u_checkout(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT void ackerman_model_impl_dae_fun_jac_x_xdot_u_release(int mem) {
}

CASADI_SYMBOL_EXPORT void ackerman_model_impl_dae_fun_jac_x_xdot_u_incref(void) {
}

CASADI_SYMBOL_EXPORT void ackerman_model_impl_dae_fun_jac_x_xdot_u_decref(void) {
}

CASADI_SYMBOL_EXPORT casadi_int ackerman_model_impl_dae_fun_jac_x_xdot_u_n_in(void) { return 6;}

CASADI_SYMBOL_EXPORT casadi_int ackerman_model_impl_dae_fun_jac_x_xdot_u_n_out(void) { return 4;}

CASADI_SYMBOL_EXPORT casadi_real ackerman_model_impl_dae_fun_jac_x_xdot_u_default_in(casadi_int i) {
  switch (i) {
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* ackerman_model_impl_dae_fun_jac_x_xdot_u_name_in(casadi_int i) {
  switch (i) {
    case 0: return "i0";
    case 1: return "i1";
    case 2: return "i2";
    case 3: return "i3";
    case 4: return "i4";
    case 5: return "i5";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* ackerman_model_impl_dae_fun_jac_x_xdot_u_name_out(casadi_int i) {
  switch (i) {
    case 0: return "o0";
    case 1: return "o1";
    case 2: return "o2";
    case 3: return "o3";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* ackerman_model_impl_dae_fun_jac_x_xdot_u_sparsity_in(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s0;
    case 2: return casadi_s1;
    case 3: return casadi_s2;
    case 4: return casadi_s2;
    case 5: return casadi_s3;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* ackerman_model_impl_dae_fun_jac_x_xdot_u_sparsity_out(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s4;
    case 2: return casadi_s5;
    case 3: return casadi_s6;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 6;
  if (sz_res) *sz_res = 4;
  if (sz_iw) *sz_iw = 0;
  if (sz_w) *sz_w = 0;
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_impl_dae_fun_jac_x_xdot_u_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 6*sizeof(const casadi_real*);
  if (sz_res) *sz_res = 4*sizeof(casadi_real*);
  if (sz_iw) *sz_iw = 0*sizeof(casadi_int);
  if (sz_w) *sz_w = 0*sizeof(casadi_real);
  return 0;
}


#ifdef __cplusplus
} /* extern "C" */
#endif
