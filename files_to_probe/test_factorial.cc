#include <gtest/gtest.h>
#include "factorial.cc"

TEST(FactorialTest, HandlesPositiveInput) {
  EXPECT_EQ(factorial(1), 1);
  EXPECT_EQ(factorial(5), 120);
  EXPECT_EQ(factorial(10), 3628800);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}