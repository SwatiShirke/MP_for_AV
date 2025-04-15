#ifndef POLYTOPES_H
#define POLYTOPES_H

#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <Eigen/Eigen>
#include <eigen3/Eigen/Dense>
#include <eigen3/Eigen/Geometry>

const int m_bot = 4;
const int n_bot = 2;
const int m_obj = 4;
const int n_obj = 2;

// class Polytope 
// {
//     private:        
//     Eigen::Matrix<double, m_obj, n_obj> A_obj;
//     Eigen::Matrix<double , m_obj, 1> B_obj;
//     float L, W;
//     Eigen::Vector3d origin;
    
//     public:
//     Polytope(Eigen::Vector2d origin , float L, float W)
//     {    
//         this->L = L;
//         this->W = W;
//         this->origin = origin;
    
//     }  

//     std::pair<Eigen::Matrix<double, m_obj, n_obj>, Eigen::Matrix<double, m_obj, 1> > get_matrices(Eigen::Vector2d origin)
//     {   
//         this->origin = origin;        
//         A_obj << -1, 0, 0, -1, 1, 0, 0, 1;
//         B_obj << -this->origin[0]+L/2, -this->origin[1]+W/2, this->origin[0]+ L/2, this->origin[1]+W/2;
//         return std::make_pair(A_obj, B_obj); 
//     } 

//     std::pair<Eigen::Matrix<double, m_obj, n_obj>, Eigen::Matrix<double, m_obj, 1> > get_matrices(void)
//     {                
//         A_obj << -1, 0, 0, -1, 1, 0, 0, 1;
//         B_obj << -this->origin[0]+L/2, -this->origin[1]+W/2, this->origin[0]+ L/2, this->origin[1]+W/2;
//         return std::make_pair(A_obj, B_obj); 
//     }
    

// };


class VD_polytope
{   
    private:
    Eigen::Matrix<double, m_bot, n_bot > A_bot;
    Eigen::Matrix<double, m_bot, 1 >  B_bot;
    float L, W;    

    public:
    VD_polytope(float L, float W)
    {
      this-> L = L;
      this-> W = W;  
    }  

    std::pair< Eigen::Matrix<double, m_bot, n_bot>, Eigen::Matrix<double, m_bot, 1> > get_matrices(void)
    {
        this->A_bot << -1, 0,  0, -1,   1, 0,   0, 1;
        this->B_bot << -L/2, -W/2, L/2, W/2;
        return std::make_pair(this-> A_bot, this-> B_bot);
    }
  
};


#endif 