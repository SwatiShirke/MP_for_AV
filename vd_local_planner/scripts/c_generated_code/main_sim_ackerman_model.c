/*
 * Copyright (c) The acados authors.
 *
 * This file is part of acados.
 *
 * The 2-Clause BSD License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.;
 */


// standard
#include <stdio.h>
#include <stdlib.h>
// acados
#include "acados/utils/print.h"
#include "acados/utils/math.h"
#include "acados_c/sim_interface.h"
#include "acados_sim_solver_ackerman_model.h"

#define NX     ACKERMAN_MODEL_NX
#define NZ     ACKERMAN_MODEL_NZ
#define NU     ACKERMAN_MODEL_NU
#define NP     ACKERMAN_MODEL_NP


int main()
{
    int status = 0;
    ackerman_model_sim_solver_capsule *capsule = ackerman_model_acados_sim_solver_create_capsule();
    status = ackerman_model_acados_sim_create(capsule);

    if (status)
    {
        printf("acados_create() returned status %d. Exiting.\n", status);
        exit(1);
    }

    sim_config *acados_sim_config = ackerman_model_acados_get_sim_config(capsule);
    sim_in *acados_sim_in = ackerman_model_acados_get_sim_in(capsule);
    sim_out *acados_sim_out = ackerman_model_acados_get_sim_out(capsule);
    void *acados_sim_dims = ackerman_model_acados_get_sim_dims(capsule);

    // initial condition
    double x_current[NX];
    x_current[0] = 0.0;
    x_current[1] = 0.0;
    x_current[2] = 0.0;
    x_current[3] = 0.0;

  
    x_current[0] = 0;
    x_current[1] = 0;
    x_current[2] = 0;
    x_current[3] = 0;
    
  


    // initial value for control input
    double u0[NU];
    u0[0] = 0.0;
    u0[1] = 0.0;
    u0[2] = 0.0;
    u0[3] = 0.0;
    u0[4] = 0.0;
    u0[5] = 0.0;
    u0[6] = 0.0;
    u0[7] = 0.0;
    u0[8] = 0.0;
    u0[9] = 0.0;
    u0[10] = 0.0;
    u0[11] = 0.0;
    u0[12] = 0.0;
    u0[13] = 0.0;
    u0[14] = 0.0;
    u0[15] = 0.0;
    u0[16] = 0.0;
    u0[17] = 0.0;
    u0[18] = 0.0;
    u0[19] = 0.0;
    u0[20] = 0.0;
    u0[21] = 0.0;
    u0[22] = 0.0;
    u0[23] = 0.0;
    u0[24] = 0.0;
    u0[25] = 0.0;
    u0[26] = 0.0;
    u0[27] = 0.0;
    u0[28] = 0.0;
    u0[29] = 0.0;
    u0[30] = 0.0;
    u0[31] = 0.0;
    u0[32] = 0.0;
    u0[33] = 0.0;
    u0[34] = 0.0;
    u0[35] = 0.0;
    u0[36] = 0.0;
    u0[37] = 0.0;
    u0[38] = 0.0;
    u0[39] = 0.0;
    u0[40] = 0.0;
    u0[41] = 0.0;
    u0[42] = 0.0;
    u0[43] = 0.0;
    // set parameters
    double p[NP];
    p[0] = 0;
    p[1] = 0;
    p[2] = 0;
    p[3] = 0;
    p[4] = 0;
    p[5] = 0;
    p[6] = 0;
    p[7] = 0;
    p[8] = 0;
    p[9] = 0;
    p[10] = 0;
    p[11] = 0;
    p[12] = 0;
    p[13] = 0;
    p[14] = 0;
    p[15] = 0;
    p[16] = 0;
    p[17] = 0;
    p[18] = 0;
    p[19] = 0;
    p[20] = 0;
    p[21] = 0;
    p[22] = 0;
    p[23] = 0;
    p[24] = 0;
    p[25] = 0;
    p[26] = 0;
    p[27] = 0;
    p[28] = 0;
    p[29] = 0;
    p[30] = 0;
    p[31] = 0;
    p[32] = 0;
    p[33] = 0;
    p[34] = 0;
    p[35] = 0;
    p[36] = 0;
    p[37] = 0;
    p[38] = 0;
    p[39] = 0;
    p[40] = 0;
    p[41] = 0;
    p[42] = 0;
    p[43] = 0;
    p[44] = 0;
    p[45] = 0;
    p[46] = 0;
    p[47] = 0;
    p[48] = 0;
    p[49] = 0;
    p[50] = 0;
    p[51] = 0;
    p[52] = 0;
    p[53] = 0;
    p[54] = 0;
    p[55] = 0;
    p[56] = 0;
    p[57] = 0;
    p[58] = 0;
    p[59] = 0;
    p[60] = 0;
    p[61] = 0;
    p[62] = 0;
    p[63] = 0;
    p[64] = 0;
    p[65] = 0;
    p[66] = 0;
    p[67] = 0;
    p[68] = 0;
    p[69] = 0;
    p[70] = 0;
    p[71] = 0;
    p[72] = 0;
    p[73] = 0;
    p[74] = 0;
    p[75] = 0;
    p[76] = 0;
    p[77] = 0;
    p[78] = 0;
    p[79] = 0;

    ackerman_model_acados_sim_update_params(capsule, p, NP);
  

  


    int n_sim_steps = 3;
    // solve ocp in loop
    for (int ii = 0; ii < n_sim_steps; ii++)
    {
        // set inputs
        sim_in_set(acados_sim_config, acados_sim_dims,
            acados_sim_in, "x", x_current);
        sim_in_set(acados_sim_config, acados_sim_dims,
            acados_sim_in, "u", u0);

        // solve
        status = ackerman_model_acados_sim_solve(capsule);
        if (status != ACADOS_SUCCESS)
        {
            printf("acados_solve() failed with status %d.\n", status);
        }

        // get outputs
        sim_out_get(acados_sim_config, acados_sim_dims,
               acados_sim_out, "x", x_current);

    

        // print solution
        printf("\nx_current, %d\n", ii);
        for (int jj = 0; jj < NX; jj++)
        {
            printf("%e\n", x_current[jj]);
        }
    }

    printf("\nPerformed %d simulation steps with acados integrator successfully.\n\n", n_sim_steps);

    // free solver
    status = ackerman_model_acados_sim_free(capsule);
    if (status) {
        printf("ackerman_model_acados_sim_free() returned status %d. \n", status);
    }

    ackerman_model_acados_sim_solver_free_capsule(capsule);

    return status;
}
