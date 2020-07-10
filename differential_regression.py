import torch

import numpy as np

from bingo.evaluation.fitness_function import VectorBasedFunction


class DifferentialRegression_TF(VectorBasedFunction):

    def __init__(self,
                 X, U, X_df, df_err,
                 df_order=1,
                 differential_weight=1.0,
                 metric="mae",
                 detect_const_solutions=True):

        super().__init__(None, metric)

        self.X = [torch.tensor(X[:, i], dtype=torch.float32)
                  for i in range(X.shape[1])]

        self.U = U  # Keep as a numpy array
        self.X_df = [
            torch.tensor(X_df[:, i], dtype=torch.float32)
            for i in range(X_df.shape[1])
        ]
        for X in self.X_df:
            X.requires_grad = True

        self.differential_weight = differential_weight
        self.detect_const_solutions = detect_const_solutions

        self.df_err = df_err

    def build_torch_graph_from_agraph(self, individual):

        commands = individual._short_command_array
        constants = individual.constants

        def evaluate(X):
            ad_stack = [None] * commands.shape[0]

            for i in range(commands.shape[0]):

                node = commands[i, 0]
                if node == 0:
                    column_idx = commands[i, 1]
                    ad_stack[i] = X[column_idx]
                elif node == 1:
                    const_idx = commands[i, 1]
                    # IMPORTANT: We need to first create the constant using numpy
                    # and then convert to tensor to avoid a memory leak. This bypasses
                    # one of tensorflows caching mechanisms for constants which causes the leak.
                    ad_stack[i] = torch.ones_like(
                        X[0], dtype=torch.float32) * constants[const_idx]
                elif node == 2:
                    t1_idx, t2_idx = commands[i, 1], commands[i, 2]
                    ad_stack[i] = ad_stack[t1_idx] + ad_stack[t2_idx]
                elif node == 3:
                    t1_idx, t2_idx = commands[i, 1], commands[i, 2]
                    ad_stack[i] = ad_stack[t1_idx] - ad_stack[t2_idx]
                elif node == 4:
                    t1_idx, t2_idx = commands[i, 1], commands[i, 2]
                    ad_stack[i] = ad_stack[t1_idx] * ad_stack[t2_idx]
                elif node == 5:
                    t1_idx, t2_idx = commands[i, 1], commands[i, 2]
                    ad_stack[i] = ad_stack[t1_idx] / ad_stack[t2_idx]
                elif node == 6:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.sin(ad_stack[t1_idx])
                elif node == 7:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.cos(ad_stack[t1_idx])
                elif node == 8:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.exp(ad_stack[t1_idx])
                elif node == 9:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.log(tf.abs(ad_stack[t1_idx]))
                elif node == 10:
                    t1_idx, t2_idx = commands[i, 1], commands[i, 2]
                    ad_stack[i] = torch.pow(
                        torch.abs(ad_stack[t1_idx]), ad_stack[t2_idx])
                elif node == 11:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.abs(ad_stack[t1_idx])
                elif node == 12:
                    t1_idx = commands[i, 1]
                    ad_stack[i] = torch.sqrt(torch.abs(ad_stack[t1_idx]))
                else:
                    raise IndexError(f"Node value {node} unrecognized")

            return ad_stack[-1]

        return evaluate

    def evaluate_fitness_vector(self, individual):

        self.eval_count += 1
        ad_graph_function = self.build_torch_graph_from_agraph(individual)
        U_hat = ad_graph_function(self.X).detach().numpy()
        error_fit = self.U[:, 0] - U_hat

        if self.X_df is not None:
            U_df = ad_graph_function(self.X_df)

            error_df = self.df_err(self.X_df, U_df).detach().numpy()

            fitness = self._metric(error_fit) + \
                self.differential_weight * self._metric(error_df)

            if self.detect_const_solutions and not np.isinf(fitness):
                random_idx = np.random.choice(list(range(U_df.shape[0])), 6)
                U_df_npy = U_df.detach().numpy()

                vals = U_df_npy[random_idx]

                residual = vals[0] - vals[1] + \
                    vals[2] - vals[3] + vals[4] - vals[5]

                if np.abs(residual) < 1e-6:
                    fitness = np.inf

            if np.isnan(fitness):
                fitness = np.inf
        else:
            fitness = self._metric(error_fit)

        return fitness
