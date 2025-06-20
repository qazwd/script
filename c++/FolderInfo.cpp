//
/*
#include <iostream>
#include <filesystem>
#include <queue>
#include <map>
#include <vector>
#include <iomanip>
#include <cmath>
#include <algorithm>

namespace fs = std::filesystem;

std::string _get_folder_name(const std::string& folder_path) {
    fs::path normalized_path = fs::path(folder_path).lexically_normal();
    return normalized_path.filename().string();
}

std::pair<int, std::map<std::string, int>> FolderAnalysis(
    const std::string& folder_path,
    int verbose = 0,
    int max_depth = -1,
    bool hidden = false,
    bool Logo = false
) {
    std::cout << "\n******--------------> 文件夹分析工具 <--------------******\n";

    if (!Logo) {
        std::cout << "\n";
    } else {
        std::cout << "******----------------> 作者：qhk <----------------******\n";
        std::cout << "******---------------> 版本：1.0.0 <---------------******\n";
        std::cout << "******--------> 功能：分析文件夹结构和信息 <--------******\n\n";
    }

    std::string folder = _get_folder_name(folder_path);
    int total_files = 0;
    std::map<std::string, int> total_file_types;
    bool analyzed = false;

    std::queue<std::pair<std::string, int>> dir_queue;
    dir_queue.push({folder_path, 0});

    if (verbose == 0 || verbose == 1) {
        std::cout << "开始遍历文件夹: " << folder << "\n";
        std::cout << std::string(50, '=') << "\n";
    }

    while (!dir_queue.empty()) {
        auto [current_dir, level] = dir_queue.front();
        dir_queue.pop();

        if (max_depth != -1 && level > max_depth) {
            continue;
        }

        std::vector<std::string> folder_names;
        int file_count = 0;
        std::map<std::string, int> current_file_types;

        try {
            for (const auto& entry : fs::directory_iterator(current_dir)) {
                std::string item = entry.path().filename().string();

                if (!hidden && item[0] == '.') {
                    continue;
                }

                if (fs::is_directory(entry.status())) {
                    folder_names.push_back(item);
                    dir_queue.push({entry.path().string(), level + 1});
                } else {
                    file_count++;
                    std::string ext = entry.path().extension().string();
                    if (ext.empty()) {
                        ext = "无扩展名";
                    } else {
                        std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
                    }
                    current_file_types[ext]++;
                    total_file_types[ext]++;
                }
            }
            total_files += file_count;
        } catch (const fs::filesystem_error& e) {
            if (verbose == 0 || verbose == 1) {
                std::cerr << "访问目录时发生错误: " << e.what() << "\n";
            }
            continue;
        } catch (...) {
            if (verbose == 0 || verbose == 1) {
                std::cerr << "发生未知错误\n";
            }
            continue;
        }

        if (verbose == 0) {
            std::string indent(level * 4, ' ');
            if (level > 0) indent = "│   " + indent.substr(4);

            std::cout << indent << "├── [层级 " << level << "] " << current_dir << "\n";
            std::cout << indent << "│   ├── 文件夹数量: " << folder_names.size() << "\n";
            std::cout << indent << "│   ├── 文件数量: " << file_count << "\n";

            if (!folder_names.empty()) {
                std::cout << indent << "│   ├── 文件夹名称:\n";
                const int per_line = 10;
                int lines = std::ceil(static_cast<double>(folder_names.size()) / per_line);
                
                for (int i = 0; i < lines; i++) {
                    int start = i * per_line;
                    int end = std::min(start + per_line, static_cast<int>(folder_names.size()));
                    std::string line;
                    for (int j = start; j < end; j++) {
                        if (j > start) line += ", ";
                        line += folder_names[j];
                    }
                    std::cout << indent << "│   │   ├── " << line << "\n";
                }
            } else {
                std::cout << indent << "│   ├── 文件夹名称: 无\n";
            }

            if (file_count > 0) {
                std::cout << indent << "│   |── 文件类型分布:\n";
                for (const auto& [type, count] : current_file_types) {
                    std::cout << indent << "│   │   ├── " << type << ": " << count << "\n";
                }
            } else {
                std::cout << indent << "│   ├── 无文件\n";
            }

            if (!folder_names.empty()) {
                std::cout << indent << "\n" << indent << "▼\n";
            } else {
                std::cout << indent << "|\n";
            }
        }

        analyzed = true;
    }

    if (verbose == 0 || verbose == 1) {
        if (verbose == 0) {
            std::cout << "\n" << std::string(50, '=') << "\n";
        }
        std::cout << "文件夹: " << folder << " 分析完成!\n";
        std::cout << "|──总文件数量: " << total_files << "\n";
        std::cout << "└──文件类型分布:\n";
        if (total_files > 0) {
            for (const auto& [type, count] : total_file_types) {
                std::cout << "    ├── " << type << ": " << count << "\n";
            }
        } else {
            std::cout << "├── 无文件\n";
        }
    }

    std::cout << "\n******------------> 文件夹内容统计工具 <------------******\n\n";

    return {total_files, total_file_types};
}

int main() {
    std::string folder_path = "D:\\hh\\code";
    auto [total_files, file_types] = FolderAnalysis(
        folder_path,
        0,    // verbose
        -1,   // max_depth (无限制)
        true, // hidden
        true  // Logo
    );
    
    return 0;
}
//*/