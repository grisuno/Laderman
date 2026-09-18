# API

## complex_leibler_transformer.py

### main (method) `def main()`
- Defined: `complex_leibler_transformer.py:2238`

### calculate (method) `def calculate(self)`
- Defined: `complex_leibler_transformer.py:199`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `complex_leibler_transformer.py:205`

### save (method) `def save(self, state, path)`
- Defined: `complex_leibler_transformer.py:212`

### load (method) `def load(self, path)`
- Defined: `complex_leibler_transformer.py:216`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `complex_leibler_transformer.py:220`

### execute (method) `def execute(self, model)`
- Defined: `complex_leibler_transformer.py:226`

### detect (method) `def detect(self, metrics)`
- Defined: `complex_leibler_transformer.py:232`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `complex_leibler_transformer.py:238`

### update (method) `def update(self, metrics)`
- Defined: `complex_leibler_transformer.py:244`

### set_seed (method) `def set_seed(seed, device)`
- Defined: `complex_leibler_transformer.py:254`

### complex_linear (method) `def complex_linear(input_real, input_imag, weight_real, weight_imag, bias_real, bias_imag)`
- Defined: `complex_leibler_transformer.py:271`

### complex_gelu (method) `def complex_gelu(real, imag)`
- Defined: `complex_leibler_transformer.py:288`

### complex_layer_norm (method) `def complex_layer_norm(real, imag, weight, bias, eps)`
- Defined: `complex_leibler_transformer.py:295`

### compute_phase (method) `def compute_phase(real, imag)`
- Defined: `complex_leibler_transformer.py:311`

### compute_magnitude (method) `def compute_magnitude(real, imag)`
- Defined: `complex_leibler_transformer.py:315`

### complex_softmax (method) `def complex_softmax(real, imag, temperature, dim)`
- Defined: `complex_leibler_transformer.py:319`

### __init__ (method) `def __init__(self, in_features, out_features, bias, init_std)`
- Defined: `complex_leibler_transformer.py:338`

### forward (method) `def forward(self, real, imag)`
- Defined: `complex_leibler_transformer.py:352`

### __init__ (method) `def __init__(self, normalized_shape, eps)`
- Defined: `complex_leibler_transformer.py:365`

### forward (method) `def forward(self, real, imag)`
- Defined: `complex_leibler_transformer.py:371`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:380`

### forward (method) `def forward(self, real, imag, mask)`
- Defined: `complex_leibler_transformer.py:404`

### _update_thermodynamic_state (method) `def _update_thermodynamic_state(self, attn_real, attn_imag)`
- Defined: `complex_leibler_transformer.py:450`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:486`

### forward (method) `def forward(self, real, imag, mask)`
- Defined: `complex_leibler_transformer.py:498`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:530`

### _init_weights (method) `def _init_weights(self)`
- Defined: `complex_leibler_transformer.py:554`

### forward (method) `def forward(self, x, mask)`
- Defined: `complex_leibler_transformer.py:564`

### get_thermodynamic_state (method) `def get_thermodynamic_state(self)`
- Defined: `complex_leibler_transformer.py:584`

### get_complex_weight_statistics (method) `def get_complex_weight_statistics(self)`
- Defined: `complex_leibler_transformer.py:610`

### create (method) `def create(modulus, train_fraction)`
- Defined: `complex_leibler_transformer.py:655`

### train_epoch (method) `def train_epoch(model, train_x, train_y, optimizer, config, device)`
- Defined: `complex_leibler_transformer.py:690`

### evaluate (method) `def evaluate(model, test_x, test_y, config, device)`
- Defined: `complex_leibler_transformer.py:724`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:755`

### calculate (method) `def calculate(self, model)`
- Defined: `complex_leibler_transformer.py:758`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:773`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `complex_leibler_transformer.py:778`

### calculate_kappa (method) `def calculate_kappa(self)`
- Defined: `complex_leibler_transformer.py:789`

### get_gradient_covariance (method) `def get_gradient_covariance(self)`
- Defined: `complex_leibler_transformer.py:809`

### get_kappa_trend (method) `def get_kappa_trend(self)`
- Defined: `complex_leibler_transformer.py:820`

### is_crystallizing (method) `def is_crystallizing(self)`
- Defined: `complex_leibler_transformer.py:830`

### reset (method) `def reset(self)`
- Defined: `complex_leibler_transformer.py:836`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:842`

### calculate (method) `def calculate(self, model, gradient_covariance)`
- Defined: `complex_leibler_transformer.py:845`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:895`

### calculate (method) `def calculate(self, model, train_x, train_y, device)`
- Defined: `complex_leibler_transformer.py:898`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:950`

### _initialize_sae (method) `def _initialize_sae(self, input_dim, device)`
- Defined: `complex_leibler_transformer.py:955`

### calculate (method) `def calculate(self, model)`
- Defined: `complex_leibler_transformer.py:961`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:989`

### calculate (method) `def calculate(self, model)`
- Defined: `complex_leibler_transformer.py:992`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1004`

### calculate (method) `def calculate(self, model)`
- Defined: `complex_leibler_transformer.py:1007`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1016`

### detect (method) `def detect(self, metrics)`
- Defined: `complex_leibler_transformer.py:1021`

### __init__ (method) `def __init__(self, model, config, optimizer)`
- Defined: `complex_leibler_transformer.py:1059`

### step (method) `def step(self, metrics)`
- Defined: `complex_leibler_transformer.py:1074`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `complex_leibler_transformer.py:1117`

### _update_optimizer_weight_decay (method) `def _update_optimizer_weight_decay(self)`
- Defined: `complex_leibler_transformer.py:1121`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1131`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `complex_leibler_transformer.py:1135`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1170`

### update (method) `def update(self, metrics)`
- Defined: `complex_leibler_transformer.py:1177`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1206`

### save (method) `def save(self, state, path)`
- Defined: `complex_leibler_transformer.py:1212`

### load (method) `def load(self, path)`
- Defined: `complex_leibler_transformer.py:1221`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `complex_leibler_transformer.py:1228`

### get_latest_path (method) `def get_latest_path(self)`
- Defined: `complex_leibler_transformer.py:1232`

### prune (method) `def prune(model, threshold)`
- Defined: `complex_leibler_transformer.py:1243`

### discretize (method) `def discretize(model, tolerance)`
- Defined: `complex_leibler_transformer.py:1263`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1297`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `complex_leibler_transformer.py:1300`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1336`

### compute_all (method) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- Defined: `complex_leibler_transformer.py:1347`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `complex_leibler_transformer.py:1432`

### reset (method) `def reset(self)`
- Defined: `complex_leibler_transformer.py:1435`

### format_kappa (method) `def format_kappa(kappa, max_display)`
- Defined: `complex_leibler_transformer.py:1446`

### format_lc (method) `def format_lc(lc)`
- Defined: `complex_leibler_transformer.py:1452`

### __init__ (method) `def __init__(self, config, seed)`
- Defined: `complex_leibler_transformer.py:1465`

### execute (method) `def execute(self, model)`
- Defined: `complex_leibler_transformer.py:1469`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1652`

### execute (method) `def execute(self, model)`
- Defined: `complex_leibler_transformer.py:1656`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:1878`

### prospect (method) `def prospect(self, total_attempts, start_seed)`
- Defined: `complex_leibler_transformer.py:1885`

### __init__ (method) `def __init__(self, config)`
- Defined: `complex_leibler_transformer.py:2021`

### _signal_handler (method) `def _signal_handler(self, signum, frame)`
- Defined: `complex_leibler_transformer.py:2029`

### run (method) `def run(self, resume_from, seed)`
- Defined: `complex_leibler_transformer.py:2033`

### __init__ (method) `def __init__(self)`
- Defined: `complex_leibler_transformer.py:2152`

### _create_argument_parser (method) `def _create_argument_parser(self)`
- Defined: `complex_leibler_transformer.py:2155`

### run (method) `def run(self)`
- Defined: `complex_leibler_transformer.py:2190`

## kappa_miner.py

### __init__ (method) `def __init__(self, config)`
- Defined: `kappa_miner.py:75`

### compute_kappa (method) `def compute_kappa(self, model, loss_fn, data_generator, n_samples, batch_size)`
- Defined: `kappa_miner.py:78`
- Doc: Compute gradient covariance condition number κ.

### predict_grokking (method) `def predict_grokking(self, kappa)`
- Defined: `kappa_miner.py:168`
- Doc: Predict whether model will grokk based on κ.

### __init__ (method) `def __init__(self, max_digits, operations, tokenizer_vocab)`
- Defined: `kappa_miner.py:214`
- Doc: Args:

### generate_batch (method) `def generate_batch(self, batch_size, operation)`
- Defined: `kappa_miner.py:240`
- Doc: Generate batch of arithmetic problems.

### _encode_number (method) `def _encode_number(self, n)`
- Defined: `kappa_miner.py:292`
- Doc: Encode number as sequence of digit tokens.

### __init__ (method) `def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_seq_len, dropout)`
- Defined: `kappa_miner.py:324`

### _init_weights (method) `def _init_weights(self)`
- Defined: `kappa_miner.py:356`
- Doc: Xavier initialization.

### forward (method) `def forward(self, x)`
- Defined: `kappa_miner.py:362`
- Doc: Args:

### __init__ (method) `def __init__(self, model, task, config)`
- Defined: `kappa_miner.py:399`

### prospect (method) `def prospect(self, early_epochs, save_checkpoints, checkpoint_dir)`
- Defined: `kappa_miner.py:417`
- Doc: Prospect for algorithmic learning using κ-mining.

### __init__ (method) `def __init__(self, model_class, task, config)`
- Defined: `kappa_miner.py:571`

### prospect_seeds (method) `def prospect_seeds(self, n_candidates, early_epochs)`
- Defined: `kappa_miner.py:579`
- Doc: Prospect multiple random seeds to find crystals.

### loss_fn (method) `def loss_fn(outputs, targets)`
- Defined: `kappa_miner.py:449`

### data_generator (method) `def data_generator(batch_size)`
- Defined: `kappa_miner.py:455`

## laderman_batch_prospection.py

### compute_kappa (method) `def compute_kappa(model, batch, num_samples)`
- Defined: `laderman_batch_prospection.py:139`
- Doc: Computa κ (número de condición de la covarianza de gradientes).

### compute_local_complexity (method) `def compute_local_complexity(model)`
- Defined: `laderman_batch_prospection.py:178`
- Doc: Computa la complejidad local (rango efectivo de U).

### compute_effective_temperature (method) `def compute_effective_temperature(model, batch, num_samples)`
- Defined: `laderman_batch_prospection.py:190`
- Doc: Computa la temperatura efectiva T_eff.

### compute_entropy (method) `def compute_entropy(model, batch, num_samples)`
- Defined: `laderman_batch_prospection.py:216`
- Doc: Computa la entropía h_bar de los gradientes.

### train_prospection_run (method) `def train_prospection_run(config, batch_size)`
- Defined: `laderman_batch_prospection.py:250`
- Doc: Ejecuta un entrenamiento corto con un batch size específico

### analyze_results (method) `def analyze_results(results, config)`
- Defined: `laderman_batch_prospection.py:409`
- Doc: Analiza los resultados de la prospección y recomienda el batch size óptimo.

### run_prospection (method) `def run_prospection(config)`
- Defined: `laderman_batch_prospection.py:536`
- Doc: Ejecuta la prospección completa de batch size.

### __post_init__ (method) `def __post_init__(self)`
- Defined: `laderman_batch_prospection.py:81`

### __init__ (method) `def __init__(self, matrix_size, num_samples, seed)`
- Defined: `laderman_batch_prospection.py:92`

### __len__ (method) `def __len__(self)`
- Defined: `laderman_batch_prospection.py:105`

### __getitem__ (method) `def __getitem__(self, idx)`
- Defined: `laderman_batch_prospection.py:108`

### __init__ (method) `def __init__(self, matrix_size, initial_slots)`
- Defined: `laderman_batch_prospection.py:115`

### forward (method) `def forward(self, input_a, input_b)`
- Defined: `laderman_batch_prospection.py:124`

### compute_discretization_margin (method) `def compute_discretization_margin(self)`
- Defined: `laderman_batch_prospection.py:129`

### tqdm (method) `def tqdm(iterable)`
- Defined: `laderman_batch_prospection.py:37`

## laderman_crystallization.py

### run_laderman_experiment (method) `def run_laderman_experiment(config)`
- Defined: `laderman_crystallization.py:1215`
- Doc: Run complete Laderman crystallization experiment.

### __post_init__ (method) `def __post_init__(self)`
- Defined: `laderman_crystallization.py:114`

### _validate_parameters (method) `def _validate_parameters(self)`
- Defined: `laderman_crystallization.py:119`

### _ensure_directories (method) `def _ensure_directories(self)`
- Defined: `laderman_crystallization.py:133`

### to_dict (method) `def to_dict(self)`
- Defined: `laderman_crystallization.py:136`

### to_dict (method) `def to_dict(self)`
- Defined: `laderman_crystallization.py:178`

### compute (method) `def compute(self, model, batch)`
- Defined: `laderman_crystallization.py:211`

### __init__ (method) `def __init__(self, num_samples)`
- Defined: `laderman_crystallization.py:226`

### compute (method) `def compute(self, model, batch)`
- Defined: `laderman_crystallization.py:229`

### _collect_gradients (method) `def _collect_gradients(self, model, input_a, input_b, target)`
- Defined: `laderman_crystallization.py:244`

### _forward_model (method) `def _forward_model(self, model, input_a, input_b)`
- Defined: `laderman_crystallization.py:261`

### _extract_bilinear_gradients (method) `def _extract_bilinear_gradients(self, model)`
- Defined: `laderman_crystallization.py:268`

### _compute_condition_number (method) `def _compute_condition_number(self, gradients)`
- Defined: `laderman_crystallization.py:276`

### __init__ (method) `def __init__(self, singular_value_threshold_ratio)`
- Defined: `laderman_crystallization.py:300`

### compute (method) `def compute(self, model, batch)`
- Defined: `laderman_crystallization.py:303`

### _compute_effective_rank (method) `def _compute_effective_rank(self, tensor)`
- Defined: `laderman_crystallization.py:313`

### compute (method) `def compute(self, model, batch)`
- Defined: `laderman_crystallization.py:331`

### _compute_superposition_coefficient (method) `def _compute_superposition_coefficient(self, u)`
- Defined: `laderman_crystallization.py:341`

### _compute_effective_feature_count (method) `def _compute_effective_feature_count(self, u)`
- Defined: `laderman_crystallization.py:347`

### __init__ (method) `def __init__(self, num_samples)`
- Defined: `laderman_crystallization.py:365`

### compute (method) `def compute(self, model, batch)`
- Defined: `laderman_crystallization.py:368`

### _collect_gradient_norms (method) `def _collect_gradient_norms(self, model, input_a, input_b, target)`
- Defined: `laderman_crystallization.py:389`

### _forward_model (method) `def _forward_model(self, model, input_a, input_b)`
- Defined: `laderman_crystallization.py:406`

### _compute_bilinear_grad_norm (method) `def _compute_bilinear_grad_norm(self, model)`
- Defined: `laderman_crystallization.py:413`

### _compute_entropy (method) `def _compute_entropy(self, values)`
- Defined: `laderman_crystallization.py:420`

### _compute_heat_capacity (method) `def _compute_heat_capacity(self, values, t_eff)`
- Defined: `laderman_crystallization.py:426`

### compute (method) `def compute(self, model, batch, effective_temperature, kappa)`
- Defined: `laderman_crystallization.py:441`

### _compute_weight_variance (method) `def _compute_weight_variance(self, u, v, w)`
- Defined: `laderman_crystallization.py:456`

### _estimate_crystal_h_bar (method) `def _estimate_crystal_h_bar(self, weight_variance, kappa)`
- Defined: `laderman_crystallization.py:460`

### _estimate_glass_h_bar (method) `def _estimate_glass_h_bar(self, t_eff, weight_variance)`
- Defined: `laderman_crystallization.py:465`

### __init__ (method) `def __init__(self, matrix_size, num_samples, seed)`
- Defined: `laderman_crystallization.py:472`

### __len__ (method) `def __len__(self)`
- Defined: `laderman_crystallization.py:486`

### __getitem__ (method) `def __getitem__(self, idx)`
- Defined: `laderman_crystallization.py:489`

### __init__ (method) `def __init__(self, config)`
- Defined: `laderman_crystallization.py:501`

### _init_weights (method) `def _init_weights(self)`
- Defined: `laderman_crystallization.py:537`

### forward (method) `def forward(self, input_a, input_b, output_attentions, return_dict)`
- Defined: `laderman_crystallization.py:546`

### get_bilinear_tensors (method) `def get_bilinear_tensors(self)`
- Defined: `laderman_crystallization.py:574`

### set_bilinear_tensors (method) `def set_bilinear_tensors(self, u, v, w)`
- Defined: `laderman_crystallization.py:577`

### compute_discretization_margin (method) `def compute_discretization_margin(self)`
- Defined: `laderman_crystallization.py:588`

### discretize (method) `def discretize(self, threshold)`
- Defined: `laderman_crystallization.py:593`

### get_weight_norm (method) `def get_weight_norm(self)`
- Defined: `laderman_crystallization.py:601`

### compute_gradient_norm (method) `def compute_gradient_norm(self)`
- Defined: `laderman_crystallization.py:604`

### prune (method) `def prune(self, model, target_slots)`
- Defined: `laderman_crystallization.py:612`

### _compute_importance (method) `def _compute_importance(self, u, v, w)`
- Defined: `laderman_crystallization.py:640`

### _select_top_k (method) `def _select_top_k(self, importance, k)`
- Defined: `laderman_crystallization.py:646`

### _verify_pruning (method) `def _verify_pruning(self, model, target_slots)`
- Defined: `laderman_crystallization.py:650`

### __init__ (method) `def __init__(self, config)`
- Defined: `laderman_crystallization.py:661`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `laderman_crystallization.py:670`

### save (method) `def save(self, model, optimizer, state, path, checkpoint_type)`
- Defined: `laderman_crystallization.py:674`

### _cleanup (method) `def _cleanup(self)`
- Defined: `laderman_crystallization.py:719`

### __init__ (method) `def __init__(self, config)`
- Defined: `laderman_crystallization.py:743`

### classify (method) `def classify(self, delta, kappa, lc, t_eff, test_accuracy)`
- Defined: `laderman_crystallization.py:746`

### __init__ (method) `def __init__(self, config)`
- Defined: `laderman_crystallization.py:787`

### update (method) `def update(self, test_accuracy, train_loss)`
- Defined: `laderman_crystallization.py:794`

### __init__ (method) `def __init__(self, config, model, train_loader, test_loader, checkpoint_manager)`
- Defined: `laderman_crystallization.py:830`

### _initialize_metric_computers (method) `def _initialize_metric_computers(self)`
- Defined: `laderman_crystallization.py:853`

### train_epoch (method) `def train_epoch(self)`
- Defined: `laderman_crystallization.py:866`

### evaluate (method) `def evaluate(self)`
- Defined: `laderman_crystallization.py:915`

### _get_model_output (method) `def _get_model_output(self, input_a, input_b)`
- Defined: `laderman_crystallization.py:941`

### compute_thermodynamic_state (method) `def compute_thermodynamic_state(self, train_metrics, test_metrics)`
- Defined: `laderman_crystallization.py:947`

### _get_sample_batch (method) `def _get_sample_batch(self)`
- Defined: `laderman_crystallization.py:1010`

### _compute_all_metrics (method) `def _compute_all_metrics(self, sample_batch)`
- Defined: `laderman_crystallization.py:1017`

### detect_confirmed_crystallization (method) `def detect_confirmed_crystallization(self)`
- Defined: `laderman_crystallization.py:1034`

### train (method) `def train(self, num_epochs)`
- Defined: `laderman_crystallization.py:1065`

### _print_training_header (method) `def _print_training_header(self, num_epochs)`
- Defined: `laderman_crystallization.py:1111`

### _update_phase_tracking (method) `def _update_phase_tracking(self, state, last_phase, consecutive_crystal_epochs)`
- Defined: `laderman_crystallization.py:1128`

### _update_progress_bar (method) `def _update_progress_bar(self, pbar, state, consecutive_crystal_epochs)`
- Defined: `laderman_crystallization.py:1140`

### _handle_grokking_event (method) `def _handle_grokking_event(self, epoch, state)`
- Defined: `laderman_crystallization.py:1163`

### _handle_crystallization_event (method) `def _handle_crystallization_event(self, epoch, state)`
- Defined: `laderman_crystallization.py:1176`

### phase2_pruning_and_discretization (method) `def phase2_pruning_and_discretization(self)`
- Defined: `laderman_crystallization.py:1188`

### tqdm (method) `def tqdm(iterable)`
- Defined: `laderman_crystallization.py:37`

## llm_kappa_miner.py

### prospect_multiple_models (method) `def prospect_multiple_models(models, config_override)`
- Defined: `llm_kappa_miner.py:554`
- Doc: Prospect multiple LLMs for algorithmic learning.

### main (method) `def main()`
- Defined: `llm_kappa_miner.py:603`

### __post_init__ (method) `def __post_init__(self)`
- Defined: `llm_kappa_miner.py:71`

### __init__ (method) `def __init__(self, tokenizer, config)`
- Defined: `llm_kappa_miner.py:89`

### format_problem (method) `def format_problem(self, a, b, op, result)`
- Defined: `llm_kappa_miner.py:94`
- Doc: Format arithmetic problem as text.

### generate_batch (method) `def generate_batch(self, batch_size)`
- Defined: `llm_kappa_miner.py:103`
- Doc: Generate batch of tokenized arithmetic problems.

### generate_for_kappa (method) `def generate_for_kappa(self, batch_size)`
- Defined: `llm_kappa_miner.py:133`
- Doc: Generate batch for κ measurement.

### __init__ (method) `def __init__(self, model, config)`
- Defined: `llm_kappa_miner.py:154`

### compute_kappa (method) `def compute_kappa(self, input_ids, labels, attention_mask)`
- Defined: `llm_kappa_miner.py:158`
- Doc: Compute κ for the LLM.

### predict_grokking (method) `def predict_grokking(self, kappa)`
- Defined: `llm_kappa_miner.py:259`
- Doc: Predict grokking based on κ (AUC=1.0 from Strassen paper).

### __init__ (method) `def __init__(self, config)`
- Defined: `llm_kappa_miner.py:297`

### train_step (method) `def train_step(self, optimizer)`
- Defined: `llm_kappa_miner.py:323`
- Doc: Single training step.

### evaluate (method) `def evaluate(self)`
- Defined: `llm_kappa_miner.py:346`
- Doc: Evaluate model and compute κ.

### prospect (method) `def prospect(self, early_stop, save_dir)`
- Defined: `llm_kappa_miner.py:376`
- Doc: Prospect for algorithmic learning using κ.

### test_arithmetic (method) `def test_arithmetic(self, n_tests)`
- Defined: `llm_kappa_miner.py:485`
- Doc: Test if the model can do arithmetic.

## seed_miner.py

### build_leiderman_config (method) `def build_leiderman_config(config)`
- Defined: `seed_miner.py:193`
- Depends on: `tran5.py`

### format_kappa (method) `def format_kappa(kappa)`
- Defined: `seed_miner.py:808`
- Depends on: `tran5.py`

### format_lc (method) `def format_lc(lc)`
- Defined: `seed_miner.py:814`
- Depends on: `tran5.py`

### main (method) `def main()`
- Defined: `seed_miner.py:1415`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self)`
- Defined: `seed_miner.py:162`
- Depends on: `tran5.py`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `seed_miner.py:168`
- Depends on: `tran5.py`

### save (method) `def save(self, state, path)`
- Defined: `seed_miner.py:175`
- Depends on: `tran5.py`

### load (method) `def load(self, path)`
- Defined: `seed_miner.py:179`
- Depends on: `tran5.py`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `seed_miner.py:183`
- Depends on: `tran5.py`

### execute (method) `def execute(self, model)`
- Defined: `seed_miner.py:189`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self, model)`
- Defined: `seed_miner.py:240`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:258`
- Depends on: `tran5.py`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `seed_miner.py:265`
- Depends on: `tran5.py`

### calculate_kappa (method) `def calculate_kappa(self)`
- Defined: `seed_miner.py:276`
- Depends on: `tran5.py`

### get_gradient_covariance (method) `def get_gradient_covariance(self)`
- Defined: `seed_miner.py:296`
- Depends on: `tran5.py`

### get_kappa_trend (method) `def get_kappa_trend(self)`
- Defined: `seed_miner.py:307`
- Depends on: `tran5.py`

### is_crystallizing (method) `def is_crystallizing(self)`
- Defined: `seed_miner.py:317`
- Depends on: `tran5.py`

### reset (method) `def reset(self)`
- Defined: `seed_miner.py:323`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:329`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self, model, gradient_covariance)`
- Defined: `seed_miner.py:332`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:379`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self, model, train_x, train_y, device)`
- Defined: `seed_miner.py:382`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:431`
- Depends on: `tran5.py`

### _initialize_sae (method) `def _initialize_sae(self, input_dim, device)`
- Defined: `seed_miner.py:436`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self, model)`
- Defined: `seed_miner.py:442`
- Depends on: `tran5.py`

### calculate (method) `def calculate(self, model)`
- Defined: `seed_miner.py:472`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:484`
- Depends on: `tran5.py`

### detect (method) `def detect(self, metrics)`
- Defined: `seed_miner.py:489`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, model, config, optimizer)`
- Defined: `seed_miner.py:519`
- Depends on: `tran5.py`

### step (method) `def step(self, metrics)`
- Defined: `seed_miner.py:534`
- Depends on: `tran5.py`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `seed_miner.py:581`
- Depends on: `tran5.py`

### _update_optimizer_weight_decay (method) `def _update_optimizer_weight_decay(self)`
- Defined: `seed_miner.py:585`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:591`
- Depends on: `tran5.py`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `seed_miner.py:597`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:636`
- Depends on: `tran5.py`

### update (method) `def update(self, metrics)`
- Defined: `seed_miner.py:643`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:672`
- Depends on: `tran5.py`

### save (method) `def save(self, state, path)`
- Defined: `seed_miner.py:678`
- Depends on: `tran5.py`

### load (method) `def load(self, path)`
- Defined: `seed_miner.py:689`
- Depends on: `tran5.py`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `seed_miner.py:696`
- Depends on: `tran5.py`

### get_latest_path (method) `def get_latest_path(self)`
- Defined: `seed_miner.py:700`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:706`
- Depends on: `tran5.py`

### compute_all (method) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- Defined: `seed_miner.py:716`
- Depends on: `tran5.py`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `seed_miner.py:800`
- Depends on: `tran5.py`

### reset (method) `def reset(self)`
- Defined: `seed_miner.py:803`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config, seed)`
- Defined: `seed_miner.py:823`
- Depends on: `tran5.py`

### execute (method) `def execute(self, model)`
- Defined: `seed_miner.py:827`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:976`
- Depends on: `tran5.py`

### execute (method) `def execute(self, model)`
- Defined: `seed_miner.py:980`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:1163`
- Depends on: `tran5.py`

### prospect (method) `def prospect(self, total_attempts, start_seed)`
- Defined: `seed_miner.py:1170`
- Depends on: `tran5.py`

### _set_seed (method) `def _set_seed(self, seed)`
- Defined: `seed_miner.py:1296`
- Depends on: `tran5.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `seed_miner.py:1305`
- Depends on: `tran5.py`

### _signal_handler (method) `def _signal_handler(self, signum, frame)`
- Defined: `seed_miner.py:1313`
- Depends on: `tran5.py`

### run (method) `def run(self, resume_from, seed)`
- Defined: `seed_miner.py:1317`
- Depends on: `tran5.py`

## superconducting_transformer.py

### main (method) `def main()`
- Defined: `superconducting_transformer.py:2236`

### calculate (method) `def calculate(self)`
- Defined: `superconducting_transformer.py:199`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `superconducting_transformer.py:205`

### save (method) `def save(self, state, path)`
- Defined: `superconducting_transformer.py:212`

### load (method) `def load(self, path)`
- Defined: `superconducting_transformer.py:216`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `superconducting_transformer.py:220`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer.py:226`

### detect (method) `def detect(self, metrics)`
- Defined: `superconducting_transformer.py:232`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `superconducting_transformer.py:238`

### update (method) `def update(self, metrics)`
- Defined: `superconducting_transformer.py:244`

### forward (method) `def forward(self, scores)`
- Defined: `superconducting_transformer.py:250`

### set_seed (method) `def set_seed(seed, device)`
- Defined: `superconducting_transformer.py:256`

### forward (method) `def forward(ctx, input_tensor, dim)`
- Defined: `superconducting_transformer.py:268`

### backward (method) `def backward(ctx, grad_output)`
- Defined: `superconducting_transformer.py:298`

### __init__ (method) `def __init__(self, dim)`
- Defined: `superconducting_transformer.py:313`

### forward (method) `def forward(self, input_tensor)`
- Defined: `superconducting_transformer.py:317`

### __init__ (method) `def __init__(self, num_units, config)`
- Defined: `superconducting_transformer.py:322`

### forward (method) `def forward(self)`
- Defined: `superconducting_transformer.py:331`

### get_expected_l0 (method) `def get_expected_l0(self)`
- Defined: `superconducting_transformer.py:344`

### get_sparsity_ratio (method) `def get_sparsity_ratio(self)`
- Defined: `superconducting_transformer.py:349`

### get_topological_charge (method) `def get_topological_charge(self)`
- Defined: `superconducting_transformer.py:354`

### update_temperature (method) `def update_temperature(self, epoch)`
- Defined: `superconducting_transformer.py:360`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:370`

### update (method) `def update(self, test_accuracy)`
- Defined: `superconducting_transformer.py:374`

### get_mu (method) `def get_mu(self)`
- Defined: `superconducting_transformer.py:388`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:393`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer.py:420`

### _update_thermodynamic_state (method) `def _update_thermodynamic_state(self, attn_weights)`
- Defined: `superconducting_transformer.py:454`

### __init__ (method) `def __init__(self, config, layer_index)`
- Defined: `superconducting_transformer.py:481`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer.py:497`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:517`

### _init_weights (method) `def _init_weights(self)`
- Defined: `superconducting_transformer.py:535`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer.py:545`

### get_thermodynamic_state (method) `def get_thermodynamic_state(self)`
- Defined: `superconducting_transformer.py:556`

### get_gate_statistics (method) `def get_gate_statistics(self)`
- Defined: `superconducting_transformer.py:580`

### get_cooper_pair_coherence (method) `def get_cooper_pair_coherence(self)`
- Defined: `superconducting_transformer.py:604`

### get_gap_energy (method) `def get_gap_energy(self)`
- Defined: `superconducting_transformer.py:652`

### get_meissner_fraction (method) `def get_meissner_fraction(self)`
- Defined: `superconducting_transformer.py:667`

### update_gate_temperatures (method) `def update_gate_temperatures(self, epoch)`
- Defined: `superconducting_transformer.py:676`

### create (method) `def create(modulus, train_fraction)`
- Defined: `superconducting_transformer.py:684`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:712`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer.py:715`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:733`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `superconducting_transformer.py:738`

### calculate_kappa (method) `def calculate_kappa(self)`
- Defined: `superconducting_transformer.py:749`

### get_gradient_covariance (method) `def get_gradient_covariance(self)`
- Defined: `superconducting_transformer.py:769`

### get_kappa_trend (method) `def get_kappa_trend(self)`
- Defined: `superconducting_transformer.py:780`

### is_crystallizing (method) `def is_crystallizing(self)`
- Defined: `superconducting_transformer.py:790`

### reset (method) `def reset(self)`
- Defined: `superconducting_transformer.py:796`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:802`

### calculate (method) `def calculate(self, model, gradient_covariance)`
- Defined: `superconducting_transformer.py:805`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:855`

### calculate (method) `def calculate(self, model, train_x, train_y, device)`
- Defined: `superconducting_transformer.py:858`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:910`

### _initialize_sae (method) `def _initialize_sae(self, input_dim, device)`
- Defined: `superconducting_transformer.py:915`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer.py:921`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:949`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer.py:952`

### __init__ (method) `def __init__(self, config, mu_scheduler)`
- Defined: `superconducting_transformer.py:964`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `superconducting_transformer.py:968`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1019`

### detect (method) `def detect(self, metrics)`
- Defined: `superconducting_transformer.py:1024`

### __init__ (method) `def __init__(self, model, config, optimizer)`
- Defined: `superconducting_transformer.py:1061`

### step (method) `def step(self, metrics)`
- Defined: `superconducting_transformer.py:1076`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `superconducting_transformer.py:1119`

### _update_optimizer_weight_decay (method) `def _update_optimizer_weight_decay(self)`
- Defined: `superconducting_transformer.py:1123`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1129`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `superconducting_transformer.py:1133`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1164`

### update (method) `def update(self, metrics)`
- Defined: `superconducting_transformer.py:1171`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1196`

### save (method) `def save(self, state, path)`
- Defined: `superconducting_transformer.py:1202`

### load (method) `def load(self, path)`
- Defined: `superconducting_transformer.py:1211`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `superconducting_transformer.py:1218`

### get_latest_path (method) `def get_latest_path(self)`
- Defined: `superconducting_transformer.py:1222`

### prune (method) `def prune(model, threshold)`
- Defined: `superconducting_transformer.py:1229`

### discretize (method) `def discretize(model, tolerance)`
- Defined: `superconducting_transformer.py:1254`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1274`

### compute_all (method) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, mu_scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- Defined: `superconducting_transformer.py:1284`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `superconducting_transformer.py:1378`

### reset (method) `def reset(self)`
- Defined: `superconducting_transformer.py:1381`

### format_kappa (method) `def format_kappa(kappa, max_display)`
- Defined: `superconducting_transformer.py:1388`

### format_lc (method) `def format_lc(lc)`
- Defined: `superconducting_transformer.py:1394`

### evaluate (method) `def evaluate(model, test_x, test_y, config, device)`
- Defined: `superconducting_transformer.py:1405`

### __init__ (method) `def __init__(self, config, seed)`
- Defined: `superconducting_transformer.py:1430`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer.py:1434`

### delta_calc_fast (method) `def delta_calc_fast(self, model)`
- Defined: `superconducting_transformer.py:1614`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1620`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer.py:1624`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:1875`

### prospect (method) `def prospect(self, total_attempts, start_seed)`
- Defined: `superconducting_transformer.py:1882`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer.py:2005`

### _signal_handler (method) `def _signal_handler(self, signum, frame)`
- Defined: `superconducting_transformer.py:2013`

### run (method) `def run(self, resume_from, seed)`
- Defined: `superconducting_transformer.py:2017`

### __init__ (method) `def __init__(self)`
- Defined: `superconducting_transformer.py:2137`

### _create_argument_parser (method) `def _create_argument_parser(self)`
- Defined: `superconducting_transformer.py:2140`

### run (method) `def run(self)`
- Defined: `superconducting_transformer.py:2180`

## superconducting_transformer2.py

### main (method) `def main()`
- Defined: `superconducting_transformer2.py:2251`

### calculate (method) `def calculate(self)`
- Defined: `superconducting_transformer2.py:199`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `superconducting_transformer2.py:205`

### save (method) `def save(self, state, path)`
- Defined: `superconducting_transformer2.py:212`

### load (method) `def load(self, path)`
- Defined: `superconducting_transformer2.py:216`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `superconducting_transformer2.py:220`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer2.py:226`

### detect (method) `def detect(self, metrics)`
- Defined: `superconducting_transformer2.py:232`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `superconducting_transformer2.py:238`

### update (method) `def update(self, metrics)`
- Defined: `superconducting_transformer2.py:244`

### forward (method) `def forward(self, scores)`
- Defined: `superconducting_transformer2.py:250`

### set_seed (method) `def set_seed(seed, device)`
- Defined: `superconducting_transformer2.py:256`

### forward (method) `def forward(ctx, input_tensor, dim)`
- Defined: `superconducting_transformer2.py:268`

### backward (method) `def backward(ctx, grad_output)`
- Defined: `superconducting_transformer2.py:298`

### __init__ (method) `def __init__(self, dim)`
- Defined: `superconducting_transformer2.py:313`

### forward (method) `def forward(self, input_tensor)`
- Defined: `superconducting_transformer2.py:317`

### __init__ (method) `def __init__(self, num_units, config)`
- Defined: `superconducting_transformer2.py:322`

### forward (method) `def forward(self)`
- Defined: `superconducting_transformer2.py:331`

### get_expected_l0 (method) `def get_expected_l0(self)`
- Defined: `superconducting_transformer2.py:344`

### get_sparsity_ratio (method) `def get_sparsity_ratio(self)`
- Defined: `superconducting_transformer2.py:349`

### get_topological_charge (method) `def get_topological_charge(self)`
- Defined: `superconducting_transformer2.py:354`

### update_temperature (method) `def update_temperature(self, epoch)`
- Defined: `superconducting_transformer2.py:360`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:370`

### update (method) `def update(self, test_accuracy)`
- Defined: `superconducting_transformer2.py:374`

### get_mu (method) `def get_mu(self)`
- Defined: `superconducting_transformer2.py:392`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:397`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer2.py:424`

### _update_thermodynamic_state (method) `def _update_thermodynamic_state(self, attn_weights)`
- Defined: `superconducting_transformer2.py:458`

### __init__ (method) `def __init__(self, config, layer_index)`
- Defined: `superconducting_transformer2.py:485`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer2.py:501`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:521`

### _init_weights (method) `def _init_weights(self)`
- Defined: `superconducting_transformer2.py:539`

### forward (method) `def forward(self, x, mask)`
- Defined: `superconducting_transformer2.py:549`

### get_thermodynamic_state (method) `def get_thermodynamic_state(self)`
- Defined: `superconducting_transformer2.py:560`

### get_gate_statistics (method) `def get_gate_statistics(self)`
- Defined: `superconducting_transformer2.py:584`

### get_cooper_pair_coherence (method) `def get_cooper_pair_coherence(self)`
- Defined: `superconducting_transformer2.py:608`

### get_gap_energy (method) `def get_gap_energy(self)`
- Defined: `superconducting_transformer2.py:656`

### get_meissner_fraction (method) `def get_meissner_fraction(self)`
- Defined: `superconducting_transformer2.py:671`

### update_gate_temperatures (method) `def update_gate_temperatures(self, epoch)`
- Defined: `superconducting_transformer2.py:680`

### create (method) `def create(modulus, train_fraction)`
- Defined: `superconducting_transformer2.py:688`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:716`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer2.py:719`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:737`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `superconducting_transformer2.py:742`

### calculate_kappa (method) `def calculate_kappa(self)`
- Defined: `superconducting_transformer2.py:753`

### get_gradient_covariance (method) `def get_gradient_covariance(self)`
- Defined: `superconducting_transformer2.py:773`

### get_kappa_trend (method) `def get_kappa_trend(self)`
- Defined: `superconducting_transformer2.py:784`

### is_crystallizing (method) `def is_crystallizing(self)`
- Defined: `superconducting_transformer2.py:794`

### reset (method) `def reset(self)`
- Defined: `superconducting_transformer2.py:800`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:806`

### calculate (method) `def calculate(self, model, gradient_covariance)`
- Defined: `superconducting_transformer2.py:809`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:859`

### calculate (method) `def calculate(self, model, train_x, train_y, device)`
- Defined: `superconducting_transformer2.py:862`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:914`

### _initialize_sae (method) `def _initialize_sae(self, input_dim, device)`
- Defined: `superconducting_transformer2.py:919`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer2.py:925`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:953`

### calculate (method) `def calculate(self, model)`
- Defined: `superconducting_transformer2.py:956`

### __init__ (method) `def __init__(self, config, mu_scheduler)`
- Defined: `superconducting_transformer2.py:968`

### compute (method) `def compute(self, model, loss_ce, epoch)`
- Defined: `superconducting_transformer2.py:972`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1048`

### detect (method) `def detect(self, metrics)`
- Defined: `superconducting_transformer2.py:1053`

### __init__ (method) `def __init__(self, model, config, optimizer)`
- Defined: `superconducting_transformer2.py:1090`

### step (method) `def step(self, metrics)`
- Defined: `superconducting_transformer2.py:1105`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `superconducting_transformer2.py:1148`

### _update_optimizer_weight_decay (method) `def _update_optimizer_weight_decay(self)`
- Defined: `superconducting_transformer2.py:1152`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1158`

### should_stop (method) `def should_stop(self, epoch, metrics)`
- Defined: `superconducting_transformer2.py:1162`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1193`

### update (method) `def update(self, metrics)`
- Defined: `superconducting_transformer2.py:1200`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1225`

### save (method) `def save(self, state, path)`
- Defined: `superconducting_transformer2.py:1231`

### load (method) `def load(self, path)`
- Defined: `superconducting_transformer2.py:1240`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `superconducting_transformer2.py:1247`

### get_latest_path (method) `def get_latest_path(self)`
- Defined: `superconducting_transformer2.py:1251`

### prune (method) `def prune(model, threshold)`
- Defined: `superconducting_transformer2.py:1258`

### discretize (method) `def discretize(model, tolerance)`
- Defined: `superconducting_transformer2.py:1283`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1303`

### compute_all (method) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, mu_scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- Defined: `superconducting_transformer2.py:1313`

### accumulate_gradient (method) `def accumulate_gradient(self, model)`
- Defined: `superconducting_transformer2.py:1407`

### reset (method) `def reset(self)`
- Defined: `superconducting_transformer2.py:1410`

### format_kappa (method) `def format_kappa(kappa, max_display)`
- Defined: `superconducting_transformer2.py:1417`

### format_lc (method) `def format_lc(lc)`
- Defined: `superconducting_transformer2.py:1423`

### evaluate (method) `def evaluate(model, test_x, test_y, config, device)`
- Defined: `superconducting_transformer2.py:1434`

### __init__ (method) `def __init__(self, config, seed)`
- Defined: `superconducting_transformer2.py:1459`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer2.py:1463`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1635`

### execute (method) `def execute(self, model)`
- Defined: `superconducting_transformer2.py:1639`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:1890`

### prospect (method) `def prospect(self, total_attempts, start_seed)`
- Defined: `superconducting_transformer2.py:1897`

### __init__ (method) `def __init__(self, config)`
- Defined: `superconducting_transformer2.py:2020`

### _signal_handler (method) `def _signal_handler(self, signum, frame)`
- Defined: `superconducting_transformer2.py:2028`

### run (method) `def run(self, resume_from, seed)`
- Defined: `superconducting_transformer2.py:2032`

### __init__ (method) `def __init__(self)`
- Defined: `superconducting_transformer2.py:2152`

### _create_argument_parser (method) `def _create_argument_parser(self)`
- Defined: `superconducting_transformer2.py:2155`

### run (method) `def run(self)`
- Defined: `superconducting_transformer2.py:2195`

## tran2.py

### run_laderman_experiment (method) `def run_laderman_experiment(config)`
- Defined: `tran2.py:916`
- Doc: Run complete Laderman crystallization experiment.

### __post_init__ (method) `def __post_init__(self)`
- Defined: `tran2.py:103`

### to_dict (method) `def to_dict(self)`
- Defined: `tran2.py:111`

### to_dict (method) `def to_dict(self)`
- Defined: `tran2.py:148`

### __init__ (method) `def __init__(self, matrix_size, num_samples, seed)`
- Defined: `tran2.py:172`

### __len__ (method) `def __len__(self)`
- Defined: `tran2.py:186`

### __getitem__ (method) `def __getitem__(self, idx)`
- Defined: `tran2.py:189`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran2.py:203`

### _init_weights (method) `def _init_weights(self)`
- Defined: `tran2.py:248`
- Doc: BERT-style initialization.

### forward (method) `def forward(self, input_a, input_b, output_attentions, return_dict)`
- Defined: `tran2.py:258`

### get_bilinear_tensors (method) `def get_bilinear_tensors(self)`
- Defined: `tran2.py:292`

### set_bilinear_tensors (method) `def set_bilinear_tensors(self, u, v, w)`
- Defined: `tran2.py:295`
- Doc: Set bilinear tensors with proper size handling.

### compute_discretization_margin (method) `def compute_discretization_margin(self)`
- Defined: `tran2.py:308`

### discretize (method) `def discretize(self, threshold)`
- Defined: `tran2.py:313`

### get_weight_norm (method) `def get_weight_norm(self)`
- Defined: `tran2.py:321`

### compute_gradient_norm (method) `def compute_gradient_norm(self)`
- Defined: `tran2.py:324`

### __init__ (method) `def __init__(self, num_samples)`
- Defined: `tran2.py:338`

### compute (method) `def compute(self, model, batch)`
- Defined: `tran2.py:341`

### compute (method) `def compute(self, model, batch)`
- Defined: `tran2.py:403`

### compute (method) `def compute(self, model, batch)`
- Defined: `tran2.py:423`

### __init__ (method) `def __init__(self, num_samples)`
- Defined: `tran2.py:444`

### compute (method) `def compute(self, model, batch)`
- Defined: `tran2.py:447`

### prune (method) `def prune(self, model, target_slots)`
- Defined: `tran2.py:500`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran2.py:550`

### should_checkpoint (method) `def should_checkpoint(self)`
- Defined: `tran2.py:558`

### save (method) `def save(self, model, optimizer, state, path, checkpoint_type)`
- Defined: `tran2.py:561`

### _cleanup (method) `def _cleanup(self)`
- Defined: `tran2.py:602`
- Doc: Remove old regular checkpoints but keep all grokking checkpoints.

### __init__ (method) `def __init__(self, config, model, train_loader, test_loader, checkpoint_manager)`
- Defined: `tran2.py:618`

### train_epoch (method) `def train_epoch(self)`
- Defined: `tran2.py:646`
- Doc: Train for one epoch with all metrics.

### evaluate (method) `def evaluate(self)`
- Defined: `tran2.py:694`
- Doc: Evaluate on test set.

### compute_thermodynamic_state (method) `def compute_thermodynamic_state(self, train_metrics, test_metrics)`
- Defined: `tran2.py:726`
- Doc: Compute complete thermodynamic state with ALL metrics.

### _detect_grokking (method) `def _detect_grokking(self, current_test_accuracy)`
- Defined: `tran2.py:788`
- Doc: Detect grokking: sudden jump in test accuracy.

### train (method) `def train(self, num_epochs)`
- Defined: `tran2.py:809`
- Doc: Phase 1: Extended training with thermodynamic monitoring.

### phase2_pruning_and_discretization (method) `def phase2_pruning_and_discretization(self)`
- Defined: `tran2.py:879`
- Doc: Phase 2: Prune to target rank and discretize.

### tqdm (method) `def tqdm(iterable)`
- Defined: `tran2.py:35`

## tran5.py

### create_modular_addition_dataset (method) `def create_modular_addition_dataset(modulus, train_fraction)`
- Defined: `tran5.py:633`
- Doc: Create dataset for modular addition task
- Imported by: `seed_miner.py`, `seed_miner.py`

### compute_kappa_from_gradient_covariance (method) `def compute_kappa_from_gradient_covariance(model, train_x, train_y, config, device)`
- Defined: `tran5.py:678`
- Doc: Compute κ = cond(Σ) where Σ is the gradient covariance matrix.
- Imported by: `seed_miner.py`, `seed_miner.py`

### compute_order_parameters (method) `def compute_order_parameters(model)`
- Defined: `tran5.py:756`
- Doc: Compute thermodynamic order parameters per paper definitions.
- Imported by: `seed_miner.py`, `seed_miner.py`

### train_epoch (method) `def train_epoch(model, train_x, train_y, optimizer, config, device)`
- Defined: `tran5.py:824`
- Doc: Train for one epoch
- Imported by: `seed_miner.py`, `seed_miner.py`

### evaluate (method) `def evaluate(model, test_x, test_y, config, device)`
- Defined: `tran5.py:868`
- Doc: Evaluate model
- Imported by: `seed_miner.py`, `seed_miner.py`

### prune_model (method) `def prune_model(model, threshold)`
- Defined: `tran5.py:905`
- Doc: Prune slots with low weight magnitudes
- Imported by: `seed_miner.py`, `seed_miner.py`

### discretize_model (method) `def discretize_model(model, tolerance)`
- Defined: `tran5.py:955`
- Doc: Attempt to discretize model weights to integers
- Imported by: `seed_miner.py`, `seed_miner.py`

### main (method) `def main()`
- Defined: `tran5.py:998`
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran5.py:75`
- Imported by: `seed_miner.py`, `seed_miner.py`

### forward (method) `def forward(self, x, mask)`
- Defined: `tran5.py:97`
- Doc: Forward pass with thermodynamic attention
- Imported by: `seed_miner.py`, `seed_miner.py`

### _update_thermodynamic_state (method) `def _update_thermodynamic_state(self)`
- Defined: `tran5.py:140`
- Doc: Update thermodynamic state variables with stable computation
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran5.py:172`
- Imported by: `seed_miner.py`, `seed_miner.py`

### forward (method) `def forward(self, x, mask)`
- Defined: `tran5.py:192`
- Doc: Forward pass with residual connections
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran5.py:210`
- Imported by: `seed_miner.py`, `seed_miner.py`

### _init_weights (method) `def _init_weights(self)`
- Defined: `tran5.py:234`
- Doc: Initialize weights with small values for stability
- Imported by: `seed_miner.py`, `seed_miner.py`

### forward (method) `def forward(self, x, mask)`
- Defined: `tran5.py:244`
- Doc: Forward pass
- Imported by: `seed_miner.py`, `seed_miner.py`

### get_thermodynamic_state (method) `def get_thermodynamic_state(self)`
- Defined: `tran5.py:268`
- Doc: Extract current thermodynamic state from all layers
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, model, config)`
- Defined: `tran5.py:297`
- Imported by: `seed_miner.py`, `seed_miner.py`

### step (method) `def step(self, metrics)`
- Defined: `tran5.py:312`
- Doc: Update temperature based on training metrics with enhanced stability
- Imported by: `seed_miner.py`, `seed_miner.py`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `tran5.py:401`
- Doc: Apply current temperature to all attention layers
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, config)`
- Defined: `tran5.py:412`
- Imported by: `seed_miner.py`, `seed_miner.py`

### update (method) `def update(self, metrics)`
- Defined: `tran5.py:439`
- Doc: Update tracker with new metrics
- Imported by: `seed_miner.py`, `seed_miner.py`

### _detect_phase (method) `def _detect_phase(self, metrics)`
- Defined: `tran5.py:455`
- Doc: Detect current thermodynamic phase based on paper-defined order parameters.
- Imported by: `seed_miner.py`, `seed_miner.py`

### _detect_grokking (method) `def _detect_grokking(self, metrics)`
- Defined: `tran5.py:489`
- Doc: Detect grokking transitions with stability requirement
- Imported by: `seed_miner.py`, `seed_miner.py`

### get_summary (method) `def get_summary(self)`
- Defined: `tran5.py:529`
- Doc: Get summary statistics
- Imported by: `seed_miner.py`, `seed_miner.py`

### __init__ (method) `def __init__(self, model, config, optimizer)`
- Defined: `tran5.py:553`
- Imported by: `seed_miner.py`, `seed_miner.py`

### step (method) `def step(self, metrics)`
- Defined: `tran5.py:566`
- Doc: Update temperature and weight_decay based on thermodynamic phase
- Imported by: `seed_miner.py`, `seed_miner.py`

### _update_model_temperatures (method) `def _update_model_temperatures(self)`
- Defined: `tran5.py:622`
- Doc: Apply current temperature to all attention layers
- Imported by: `seed_miner.py`, `seed_miner.py`

### _update_optimizer_weight_decay (method) `def _update_optimizer_weight_decay(self)`
- Defined: `tran5.py:627`
- Doc: Apply current weight_decay (pressure) to optimizer
- Imported by: `seed_miner.py`, `seed_miner.py`
