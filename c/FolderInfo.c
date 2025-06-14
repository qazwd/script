#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <errno.h>
#include <stdbool.h>
#include <math.h>
#include <ctype.h>

// 最大路径长度
#define MAX_PATH_LEN 4096
// 最大文件类型数量
#define MAX_FILE_TYPES 100
// 每行显示的文件夹数量
#define FOLDERS_PER_LINE 10

// 文件类型统计结构
typedef struct {
    char ext[20];
    int count;
} FileTypeCount;

// 文件夹分析结果结构
typedef struct {
    int total_files;
    FileTypeCount file_types[MAX_FILE_TYPES];
    int file_type_count;
} AnalysisResult;

// 队列节点结构（用于BFS遍历）
typedef struct QueueNode {
    char path[MAX_PATH_LEN];
    int depth;
    struct QueueNode* next;
} QueueNode;

// 队列结构
typedef struct {
    QueueNode* front;
    QueueNode* rear;
} Queue;

// 初始化队列
void init_queue(Queue* q) {
    q->front = q->rear = NULL;
}

// 入队操作
void enqueue(Queue* q, const char* path, int depth) {
    QueueNode* newNode = (QueueNode*)malloc(sizeof(QueueNode));
    if (!newNode) {
        perror("内存分配失败");
        exit(EXIT_FAILURE);
    }
    
    strncpy(newNode->path, path, MAX_PATH_LEN - 1);
    newNode->path[MAX_PATH_LEN - 1] = '\0';
    newNode->depth = depth;
    newNode->next = NULL;
    
    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        q->rear->next = newNode;
        q->rear = newNode;
    }
}

// 出队操作
QueueNode* dequeue(Queue* q) {
    if (q->front == NULL) {
        return NULL;
    }
    
    QueueNode* temp = q->front;
    q->front = q->front->next;
    
    if (q->front == NULL) {
        q->rear = NULL;
    }
    
    return temp;
}

// 检查队列是否为空
bool is_queue_empty(Queue* q) {
    return q->front == NULL;
}

// 释放队列内存
void free_queue(Queue* q) {
    while (!is_queue_empty(q)) {
        QueueNode* node = dequeue(q);
        free(node);
    }
}

// 获取路径的最后一部分（文件夹名）
const char* get_folder_name(const char* path) {
    const char* base = strrchr(path, '/');
    if (base) {
        return base + 1;
    }
    return path;
}

// 添加或更新文件类型统计
void update_file_type(AnalysisResult* result, const char* ext) {
    // 转换为小写
    char lower_ext[20] = {0};
    for (int i = 0; ext[i]; i++) {
        lower_ext[i] = tolower(ext[i]);
    }
    
    // 查找是否已存在
    for (int i = 0; i < result->file_type_count; i++) {
        if (strcmp(result->file_types[i].ext, lower_ext) == 0) {
            result->file_types[i].count++;
            return;
        }
    }
    
    // 添加新类型
    if (result->file_type_count < MAX_FILE_TYPES) {
        strncpy(result->file_types[result->file_type_count].ext, lower_ext, 19);
        result->file_types[result->file_type_count].ext[19] = '\0';
        result->file_types[result->file_type_count].count = 1;
        result->file_type_count++;
    }
}

// 文件夹分析函数
AnalysisResult folder_analysis(const char* folder_path, int verbose, int max_depth, bool hidden, bool logo) {
    AnalysisResult result = {0};
    Queue queue;
    init_queue(&queue);
    
    // 打印标题
    printf("\n******--------------> 文件夹分析工具 <--------------******\n");
    
    // 打印Logo
    if (logo) {
        printf("******----------------> 作者：qhk <----------------******\n");
        printf("******---------------> 版本：1.0.0 <---------------******\n");
        printf("******--------> 功能：分析文件夹结构和信息 <--------******\n\n");
    } else {
        printf("\n");
    }
    
    // 获取文件夹名称
    const char* folder_name = get_folder_name(folder_path);
    
    // 打印开始信息
    if (verbose == 0 || verbose == 1) {
        printf("开始遍历文件夹: %s\n", folder_name);
        for (int i = 0; i < 50; i++) printf("=");
        printf("\n");
    }
    
    // 将起始路径加入队列
    enqueue(&queue, folder_path, 0);
    
    // BFS遍历目录
    while (!is_queue_empty(&queue)) {
        QueueNode* current = dequeue(&queue);
        if (!current) continue;
        
        char current_dir[MAX_PATH_LEN];
        strcpy(current_dir, current->path);
        int level = current->depth;
        free(current);
        
        // 检查深度限制
        if (max_depth > 0 && level > max_depth) {
            continue;
        }
        
        DIR* dir = opendir(current_dir);
        if (!dir) {
            // 错误处理
            if (verbose == 0 || verbose == 1) {
                if (errno == EACCES) {
                    printf("无权限访问目录: %s\n", current_dir);
                } else if (errno == ENOENT) {
                    printf("目录不存在: %s\n", current_dir);
                } else {
                    printf("访问目录时发生错误: %s\n", strerror(errno));
                }
            }
            continue;
        }
        
        // 当前目录统计
        int folder_count = 0;
        int file_count = 0;
        char folder_names[100][256]; // 存储子文件夹名称
        FileTypeCount current_file_types[MAX_FILE_TYPES] = {0};
        int current_file_type_count = 0;
        
        struct dirent* entry;
        while ((entry = readdir(dir)) != NULL) {
            // 跳过 "." 和 ".."
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0) {
                continue;
            }
            
            // 跳过隐藏文件（如果需要）
            if (!hidden && entry->d_name[0] == '.') {
                continue;
            }
            
            // 构建完整路径
            char full_path[MAX_PATH_LEN];
            snprintf(full_path, sizeof(full_path), "%s/%s", current_dir, entry->d_name);
            
            // 检查是否为目录
            struct stat path_stat;
            if (stat(full_path, &path_stat) == 0) {
                if (S_ISDIR(path_stat.st_mode)) {
                    // 目录处理
                    if (folder_count < 100) {
                        strncpy(folder_names[folder_count], entry->d_name, 255);
                        folder_names[folder_count][255] = '\0';
                        folder_count++;
                    }
                    
                    // 加入队列
                    enqueue(&queue, full_path, level + 1);
                } else {
                    // 文件处理
                    file_count++;
                    result.total_files++;
                    
                    // 获取文件扩展名
                    const char* dot = strrchr(entry->d_name, '.');
                    if (dot && dot != entry->d_name) {
                        update_file_type(&result, dot);
                    } else {
                        update_file_type(&result, "无扩展名");
                    }
                }
            }
        }
        closedir(dir);
        
        // 详细模式输出
        if (verbose == 0) {
            // 生成缩进
            char indent[256] = {0};
            for (int i = 0; i < level; i++) {
                strcat(indent, "│   ");
            }
            
            // 输出当前目录信息
            printf("%s├── [层级 %d] %s\n", indent, level, current_dir);
            printf("%s│   ├── 文件夹数量: %d\n", indent, folder_count);
            printf("%s│   ├── 文件数量: %d\n", indent, file_count);
            
            // 输出文件夹名称
            if (folder_count > 0) {
                printf("%s│   ├── 文件夹名称:\n", indent);
                
                int lines = ceil((double)folder_count / FOLDERS_PER_LINE);
                for (int i = 0; i < lines; i++) {
                    char folders_line[1024] = {0};
                    int start = i * FOLDERS_PER_LINE;
                    int end = (i + 1) * FOLDERS_PER_LINE;
                    if (end > folder_count) end = folder_count;
                    
                    for (int j = start; j < end; j++) {
                        strcat(folders_line, folder_names[j]);
                        if (j < end - 1) {
                            strcat(folders_line, ", ");
                        }
                    }
                    
                    printf("%s│   │   ├── %s\n", indent, folders_line);
                }
            } else {
                printf("%s│   ├── 文件夹名称: 无\n", indent);
            }
            
            // 输出文件类型分布
            if (file_count > 0) {
                printf("%s│   |── 文件类型分布:\n", indent);
                for (int i = 0; i < result.file_type_count; i++) {
                    printf("%s│   │   ├── %s: %d\n", indent, 
                           result.file_types[i].ext, result.file_types[i].count);
                }
            } else {
                printf("%s│   │   ├── 无文件\n", indent);
            }
            
            // 输出文件夹结束提示
            if (folder_count > 0) {
                printf("%s\n%s▼\n", indent, indent);
            } else {
                printf("%s|\n", indent);
            }
        }
    }
    
    // 输出总统计信息
    if (verbose == 0 || verbose == 1) {
        if (verbose == 0) {
            for (int i = 0; i < 50; i++) printf("=");
            printf("\n");
        }
        
        printf("文件夹: %s 分析完成!\n", folder_name);
        printf("|——总文件数量: %d\n", result.total_files);
        printf("└──文件类型分布:\n");
        
        if (result.total_files > 0) {
            for (int i = 0; i < result.file_type_count; i++) {
                printf("    ├── %s: %d\n", result.file_types[i].ext, result.file_types[i].count);
            }
        } else {
            printf("    ├── 无文件\n");
        }
    }
    
    printf("\n******------------> 文件夹内容统计工具 <------------******\n\n");
    
    // 清理队列
    free_queue(&queue);
    
    return result;
}

int main() {
    const char* folder_path = "D:/hh/code"; // 替换为您的文件夹路径
    
    // 分析目录结构
    AnalysisResult result = folder_analysis(
        folder_path,
        0,      // verbose=0 打印详细信息
        -1,     // max_depth=-1 表示不限制深度
        true,   // hidden=true 包含隐藏文件
        true    // logo=true 打印Logo信息
    );
    
    // 输出结果摘要
    printf("总文件数: %d\n", result.total_files);
    printf("文件类型数量: %d\n", result.file_type_count);
    
    return 0;
}