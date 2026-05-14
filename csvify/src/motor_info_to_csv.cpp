#include <rclcpp/rclcpp.hpp>
#include <fstream>
#include <string>
#include <algorithm>
#include <memory>

// Replace with your actual message header
#include <phoenix_ros_driver/msg/talon_info.hpp>

class CsvLoggerNode : public rclcpp::Node
{
public:
  using MsgT = phoenix_ros_driver::msg::TalonInfo;

  CsvLoggerNode(const std::string &node_name, const std::string &topic_name,
                const std::string &csv_filename = "log.csv")
      : Node(node_name), topic_name_(topic_name)
  {
    // Open CSV file
    file_.open(csv_filename, std::ios::out | std::ios::trunc);

    if (!file_.is_open())
    {
      RCLCPP_ERROR(this->get_logger(), "Failed to open CSV file");
      throw std::runtime_error("Failed to open CSV file");
    }

    // Write header
    file_ << "sec,nsec,pos,vel,acc,dev_tmp,proc_tmp,bus_voltage,supply_current,"
          << "output_percent,output_voltage,output_current,"
          << "motor_state,bridge_mode,control_mode,enabled\n";

    // QOS: Best effort + Volatile
    auto my_qos = rclcpp::QoS(10).best_effort().durability_volatile();

    sub_ = this->create_subscription<MsgT>(
        topic_name_,
        my_qos,
        [this](const MsgT &msg)
        {
          this->callback(msg);
        });

    RCLCPP_INFO(this->get_logger(), "Subscribed to %s", topic_name_.c_str());
  }

  ~CsvLoggerNode()
  {
    if (file_.is_open())
    {
      file_.close();
    }
  }

private:
  void callback(const MsgT &msg)
  {
    const auto &stamp = msg.header.stamp;

    // Decode "enabled" from status bitmask
    // STATUS_PHX_ENABLED = 1
    bool enabled = (msg.status & 0x01) != 0;

    file_
        << stamp.sec << ","
        << stamp.nanosec << ","
        << msg.position << ","
        << msg.velocity << ","
        << msg.acceleration << ","
        << msg.device_temp << ","
        << msg.processor_temp << ","
        << msg.bus_voltage << ","
        << msg.supply_current << ","
        << msg.output_percent << ","
        << msg.output_voltage << ","
        << msg.output_current << ","
        << static_cast<int>(msg.motor_state) << ","
        << static_cast<int>(msg.bridge_mode) << ","
        << static_cast<int>(msg.control_mode) << ","
        << enabled
        << '\n';
  }

  std::string topic_name_;
  rclcpp::Subscription<MsgT>::SharedPtr sub_;
  std::ofstream file_;
};

int main(int argc, char *argv[])
{

  rclcpp::init(argc, argv);

  std::string topics[] = {
      "/lance/hopper_act/info",
      "/lance/hopper_act_left/info",
      "/lance/hopper_act_right/info",
      "/lance/hopper_belt/info",
      "/lance/track_left/info",
      "/lance/track_right/info",
      "/lance/trencher/info"};

  std::vector<std::shared_ptr<CsvLoggerNode>> nodes;

  rclcpp::executors::SingleThreadedExecutor executor;
  for (const auto &topic : topics)
  {
    auto fpath = topic;
    std::replace(fpath.begin(), fpath.end(), '/', '_');
    fpath.erase(fpath.begin());
    auto name = fpath;
    fpath.append(".csv");
    auto node = std::make_shared<CsvLoggerNode>(name, topic, fpath);
    nodes.push_back(node);
    executor.add_node(node);
  }

  executor.spin();

  rclcpp::shutdown();
  return 0;
}