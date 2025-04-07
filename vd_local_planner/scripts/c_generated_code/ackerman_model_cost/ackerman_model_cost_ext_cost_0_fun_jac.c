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
  #define CASADI_PREFIX(ID) ackerman_model_cost_ext_cost_0_fun_jac_ ## ID
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
static const casadi_int casadi_s1[7] = {3, 1, 0, 3, 0, 1, 2};
static const casadi_int casadi_s2[3] = {0, 0, 0};
static const casadi_int casadi_s3[11] = {7, 1, 0, 7, 0, 1, 2, 3, 4, 5, 6};
static const casadi_int casadi_s4[5] = {1, 1, 0, 1, 0};

/* ackerman_model_cost_ext_cost_0_fun_jac:(i0[4],i1[3],i2[],i3[7])->(o0,o1[7]) */
static int casadi_f0(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem) {
  casadi_real a0, a1, a10, a11, a12, a13, a14, a15, a16, a17, a18, a2, a3, a4, a5, a6, a7, a8, a9;
  a0=100.;
  a1=arg[3]? arg[3][0] : 0;
  a2=arg[0]? arg[0][0] : 0;
  a1=(a1-a2);
  a2=casadi_sq(a1);
  a2=(a0*a2);
  a3=arg[3]? arg[3][1] : 0;
  a4=arg[0]? arg[0][1] : 0;
  a3=(a3-a4);
  a4=casadi_sq(a3);
  a4=(a0*a4);
  a2=(a2+a4);
  a4=arg[3]? arg[3][3] : 0;
  a5=arg[0]? arg[0][3] : 0;
  a4=(a4-a5);
  a5=casadi_sq(a4);
  a5=(a0*a5);
  a2=(a2+a5);
  a5=1.;
  a6=arg[3]? arg[3][2] : 0;
  a7=arg[0]? arg[0][2] : 0;
  a6=(a6-a7);
  a7=cos(a6);
  a5=(a5-a7);
  a7=casadi_sq(a5);
  a7=(a0*a7);
  a2=(a2+a7);
  a7=1.0000000000000000e-08;
  a8=arg[3]? arg[3][4] : 0;
  a9=arg[1]? arg[1][0] : 0;
  a8=(a8-a9);
  a10=casadi_sq(a8);
  a10=(a7*a10);
  a11=arg[3]? arg[3][5] : 0;
  a12=arg[1]? arg[1][1] : 0;
  a11=(a11-a12);
  a13=casadi_sq(a11);
  a13=(a7*a13);
  a10=(a10+a13);
  a13=arg[3]? arg[3][6] : 0;
  a14=arg[1]? arg[1][2] : 0;
  a13=(a13-a14);
  a15=casadi_sq(a13);
  a15=(a7*a15);
  a10=(a10+a15);
  a15=2000.;
  a16=casadi_sq(a9);
  a16=(a15*a16);
  a17=1000.;
  a18=casadi_sq(a12);
  a18=(a17*a18);
  a16=(a16+a18);
  a18=casadi_sq(a14);
  a18=(a17*a18);
  a16=(a16+a18);
  a10=(a10+a16);
  a2=(a2+a10);
  if (res[0]!=0) res[0][0]=a2;
  a9=(a9+a9);
  a15=(a15*a9);
  a8=(a8+a8);
  a8=(a7*a8);
  a15=(a15-a8);
  if (res[1]!=0) res[1][0]=a15;
  a12=(a12+a12);
  a12=(a17*a12);
  a11=(a11+a11);
  a11=(a7*a11);
  a12=(a12-a11);
  if (res[1]!=0) res[1][1]=a12;
  a14=(a14+a14);
  a17=(a17*a14);
  a13=(a13+a13);
  a7=(a7*a13);
  a17=(a17-a7);
  if (res[1]!=0) res[1][2]=a17;
  a1=(a1+a1);
  a1=(a0*a1);
  a1=(-a1);
  if (res[1]!=0) res[1][3]=a1;
  a3=(a3+a3);
  a3=(a0*a3);
  a3=(-a3);
  if (res[1]!=0) res[1][4]=a3;
  a6=sin(a6);
  a5=(a5+a5);
  a5=(a0*a5);
  a6=(a6*a5);
  a6=(-a6);
  if (res[1]!=0) res[1][5]=a6;
  a4=(a4+a4);
  a0=(a0*a4);
  a0=(-a0);
  if (res[1]!=0) res[1][6]=a0;
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac(const casadi_real** arg, casadi_real** res, casadi_int* iw, casadi_real* w, int mem){
  return casadi_f0(arg, res, iw, w, mem);
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac_alloc_mem(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac_init_mem(int mem) {
  return 0;
}

CASADI_SYMBOL_EXPORT void ackerman_model_cost_ext_cost_0_fun_jac_free_mem(int mem) {
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac_checkout(void) {
  return 0;
}

CASADI_SYMBOL_EXPORT void ackerman_model_cost_ext_cost_0_fun_jac_release(int mem) {
}

CASADI_SYMBOL_EXPORT void ackerman_model_cost_ext_cost_0_fun_jac_incref(void) {
}

CASADI_SYMBOL_EXPORT void ackerman_model_cost_ext_cost_0_fun_jac_decref(void) {
}

CASADI_SYMBOL_EXPORT casadi_int ackerman_model_cost_ext_cost_0_fun_jac_n_in(void) { return 4;}

CASADI_SYMBOL_EXPORT casadi_int ackerman_model_cost_ext_cost_0_fun_jac_n_out(void) { return 2;}

CASADI_SYMBOL_EXPORT casadi_real ackerman_model_cost_ext_cost_0_fun_jac_default_in(casadi_int i) {
  switch (i) {
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* ackerman_model_cost_ext_cost_0_fun_jac_name_in(casadi_int i) {
  switch (i) {
    case 0: return "i0";
    case 1: return "i1";
    case 2: return "i2";
    case 3: return "i3";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const char* ackerman_model_cost_ext_cost_0_fun_jac_name_out(casadi_int i) {
  switch (i) {
    case 0: return "o0";
    case 1: return "o1";
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* ackerman_model_cost_ext_cost_0_fun_jac_sparsity_in(casadi_int i) {
  switch (i) {
    case 0: return casadi_s0;
    case 1: return casadi_s1;
    case 2: return casadi_s2;
    case 3: return casadi_s3;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT const casadi_int* ackerman_model_cost_ext_cost_0_fun_jac_sparsity_out(casadi_int i) {
  switch (i) {
    case 0: return casadi_s4;
    case 1: return casadi_s3;
    default: return 0;
  }
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac_work(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 4;
  if (sz_res) *sz_res = 2;
  if (sz_iw) *sz_iw = 0;
  if (sz_w) *sz_w = 0;
  return 0;
}

CASADI_SYMBOL_EXPORT int ackerman_model_cost_ext_cost_0_fun_jac_work_bytes(casadi_int *sz_arg, casadi_int* sz_res, casadi_int *sz_iw, casadi_int *sz_w) {
  if (sz_arg) *sz_arg = 4*sizeof(const casadi_real*);
  if (sz_res) *sz_res = 2*sizeof(casadi_real*);
  if (sz_iw) *sz_iw = 0*sizeof(casadi_int);
  if (sz_w) *sz_w = 0*sizeof(casadi_real);
  return 0;
}


#ifdef __cplusplus
} /* extern "C" */
#endif
