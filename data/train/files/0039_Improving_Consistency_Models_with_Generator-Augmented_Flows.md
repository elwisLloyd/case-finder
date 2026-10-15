# Improving Consistency Models with Generator-Augmented Flows

Источник: https://medium.com/criteo-engineering/improving-consistency-models-with-generator-augmented-flows-abc2ae135506

Improving Consistency Models with Generator-Augmented Flows
Delivering more personalized ads in real-time — boosting engagement and cutting infrastructure costs.
This Research Card presents Generator-Augmented Flows (GC), a technique improving consistency models, which are state-of-the-art models for fast image and video generation. For Criteo, this could mean delivering more personalized ads in real time — boosting engagement and cutting infrastructure costs.
- Title: Improving Consistency Models with Generator-Augmented Flows
- Authors: Thibaut Issenhuth, Sangchul Lee, Ludovic Dos Santos, Jean-Yves Franceschi, Chansoo Kim, Alain Rakotomamonjy
- Team: R&D — CAIL — AI Foundations — Commerce Foundation Models
- Revue: ICML 2025
- Status: Accepted
- Category: Computer Vision
Get Criteo Tech’s stories in your inbox
Join Medium for free to get updates from this writer.
Why did we work on this topic?
Classic diffusion-based generators require dozens of iterative steps to produce a final sample, which is too slow for real-time ad personalization and large-scale inference pipelines. On the opposite, CMs promise inference speed but suffer from unstable training. Our goal was to investigate this training stability, to improve one-step CMs.
What did we find? What did we achieve?
CMs can be trained in two modes: (i) distillation, by directly imitating a pre‑trained diffusion model, or (ii) from scratch, without access to a pre‑trained model. (ii) is an appealing option as it does not require a preliminary diffusion training. Yet, are these two training modes truly equivalent?
We show they are not. When a CM is trained from scratch, we identify an extra regularisation term on the generator deviating its training from the distillation setting. To alleviate this discrepancy, we introduce a simple fix called Generator‑Augmented Flows: we feed the model’s own endpoint predictions back into the data–noise coupling that defines its training loss.
As a result, Generator‑Augmented Flows speed up convergence and boost final performance. More broadly, these findings highlight the value of designing noise–data couplings that lower stochasticity during CM training.
How did we proceed?
We analysed the difference between the distillation setting, which is the ideal setting, and the “from scratch” setting. We found out a key difference in the two settings, which explains training instabilities. From here, we designed “generator-augmented flows” to reduce the gap between the two settings, in order to improve the “from scratch” setting.
What is the originality here?
Generator-Augmented Flows transform the way models learn by using their own outputs as a guide, much like a student using its own answers. This self-reinforcement loop is unique and drives faster, more efficient training. For Criteo, this could mean quicker training and fine-tuning of high-quality generative models, leading to more engaging and diverse ad variations while significantly reducing GPU consumption.
