export SQUAD_DIR=/home/tapati/Zenith_QA_System/QuestionAnswering/train
export DATA_DIR=/home/tapati/Zenith_QA_System/static/dataset/qa
export MODEL_DIR=/home/tapati/Zenith_QA_System/static/model
export SAVE_DIR=/home/tapati/Zenith_QA_System/static/qa_output
python $SQUAD_DIR/train.py \
    --model_type roberta \
    --model_name_or_path $MODEL_DIR/phobert-base \
    --do_train \
    --do_eval \
    --no_cuda\
    --version_2_with_negative \
    --do_lower_case \
    --train_file $DATA_DIR/merged_train_dataset.json \
    --predict_file $DATA_DIR/merged_test_dataset.json \
    --learning_rate 2e-5 \
    --num_train_epochs 10 \
    --max_seq_length 384 \
    --doc_stride 128 \
    --output_dir SAVE_DIR \
    --per_gpu_eval_batch_size=2  \
    --per_gpu_train_batch_size=2   \
    --save_steps 5000