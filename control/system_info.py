#!/usr/bin/env python3
"""
System Information and Diagnostics Module for Shadow AI
Provides comprehensive system monitoring and diagnostics
"""

import os
import psutil
import platform
import socket
import subprocess
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class SystemDiagnostics:
    """System information and diagnostics"""
    
    def __init__(self):
        self.system_info = self.get_basic_system_info()
    
    def get_basic_system_info(self) -> Dict:
        """Get basic system information"""
        try:
            return {
                'os': platform.system(),
                'os_version': platform.version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=True)
            }
        except Exception as e:
            logging.error(f"Error getting system info: {e}")
            return {}
    
    def get_cpu_info(self) -> Dict:
        """Get detailed CPU information"""
        try:
            cpu_freq = psutil.cpu_freq()
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            
            return {
                'cpu_percent_total': psutil.cpu_percent(interval=1),
                'cpu_percent_per_core': cpu_percent,
                'cpu_frequency_current': cpu_freq.current if cpu_freq else None,
                'cpu_frequency_min': cpu_freq.min if cpu_freq else None,
                'cpu_frequency_max': cpu_freq.max if cpu_freq else None,
                'cpu_count_physical': psutil.cpu_count(logical=False),
                'cpu_count_logical': psutil.cpu_count(logical=True),
                'load_average': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
        except Exception as e:
            logging.error(f"Error getting CPU info: {e}")
            return {}
    
    def get_memory_info(self) -> Dict:
        """Get memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'percentage': memory.percent,
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_percentage': swap.percent
            }
        except Exception as e:
            logging.error(f"Error getting memory info: {e}")
            return {}
    
    def get_disk_info(self) -> List[Dict]:
        """Get disk space information"""
        try:
            disk_info = []
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'percentage': round((usage.used / usage.total) * 100, 1)
                    })
                except PermissionError:
                    continue
                    
            return disk_info
        except Exception as e:
            logging.error(f"Error getting disk info: {e}")
            return []
    
    def get_network_info(self) -> Dict:
        """Get network information"""
        try:
            network_stats = psutil.net_io_counters()
            network_interfaces = psutil.net_if_addrs()
            
            interfaces = {}
            for interface, addresses in network_interfaces.items():
                interfaces[interface] = []
                for addr in addresses:
                    interfaces[interface].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
            
            return {
                'bytes_sent': network_stats.bytes_sent,
                'bytes_received': network_stats.bytes_recv,
                'packets_sent': network_stats.packets_sent,
                'packets_received': network_stats.packets_recv,
                'interfaces': interfaces,
                'hostname': socket.gethostname(),
                'ip_address': socket.gethostbyname(socket.gethostname())
            }
        except Exception as e:
            logging.error(f"Error getting network info: {e}")
            return {}
    
    def get_running_processes(self, limit: int = 20) -> List[Dict]:
        """Get list of running processes"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info
                    proc_info['memory_mb'] = round(proc.memory_info().rss / (1024**2), 2)
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            return processes[:limit]
            
        except Exception as e:
            logging.error(f"Error getting processes: {e}")
            return []
    
    def get_startup_programs(self) -> List[str]:
        """Get list of startup programs"""
        try:
            startup_programs = []
            
            # Windows startup locations
            startup_paths = [
                os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup'),
                'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
            ]
            
            for path in startup_paths:
                if os.path.exists(path):
                    for item in os.listdir(path):
                        startup_programs.append(item)
            
            return startup_programs
            
        except Exception as e:
            logging.error(f"Error getting startup programs: {e}")
            return []
    
    def get_installed_software(self) -> List[str]:
        """Get list of installed software (Windows)"""
        try:
            installed_software = []
            
            # Use Windows Registry to get installed programs
            try:
                import winreg
                
                registry_keys = [
                    winreg.HKEY_LOCAL_MACHINE,
                    winreg.HKEY_CURRENT_USER
                ]
                
                subkey_paths = [
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
                ]
                
                for hkey in registry_keys:
                    for subkey_path in subkey_paths:
                        try:
                            with winreg.OpenKey(hkey, subkey_path) as key:
                                for i in range(winreg.QueryInfoKey(key)[0]):
                                    try:
                                        subkey_name = winreg.EnumKey(key, i)
                                        with winreg.OpenKey(key, subkey_name) as subkey:
                                            try:
                                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                                installed_software.append(display_name)
                                            except FileNotFoundError:
                                                continue
                                    except OSError:
                                        continue
                        except OSError:
                            continue
                            
            except ImportError:
                # Fallback for non-Windows systems
                pass
            
            return list(set(installed_software))[:50]  # Limit and remove duplicates
            
        except Exception as e:
            logging.error(f"Error getting installed software: {e}")
            return []
    
    def check_system_health(self) -> Dict:
        """Perform system health check"""
        try:
            health_status = {
                'overall_status': 'Good',
                'warnings': [],
                'errors': [],
                'recommendations': []
            }
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                health_status['warnings'].append(f"High CPU usage: {cpu_percent}%")
                health_status['overall_status'] = 'Warning'
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > 90:
                health_status['warnings'].append(f"High memory usage: {memory.percent}%")
                health_status['overall_status'] = 'Warning'
            
            # Check disk space
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    percent_used = (usage.used / usage.total) * 100
                    if percent_used > 90:
                        health_status['warnings'].append(f"Low disk space on {partition.device}: {percent_used:.1f}% used")
                        health_status['overall_status'] = 'Warning'
                except PermissionError:
                    continue
            
            # Check system temperature (if available)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current > 80:  # 80°C threshold
                                health_status['warnings'].append(f"High temperature on {name}: {entry.current}°C")
                                health_status['overall_status'] = 'Warning'
            except AttributeError:
                pass  # Temperature sensors not available
            
            # Add recommendations
            if cpu_percent > 80:
                health_status['recommendations'].append("Consider closing unnecessary applications to reduce CPU usage")
            
            if memory.percent > 80:
                health_status['recommendations'].append("Consider closing memory-intensive applications")
            
            # Check if there are any errors
            if health_status['warnings']:
                if any('High' in warning or 'Low' in warning for warning in health_status['warnings']):
                    health_status['overall_status'] = 'Critical' if cpu_percent > 95 or memory.percent > 95 else 'Warning'
            
            return health_status
            
        except Exception as e:
            logging.error(f"Error checking system health: {e}")
            return {'overall_status': 'Error', 'error': str(e)}
    
    def get_system_uptime(self) -> str:
        """Get system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return f"{days} days, {hours} hours, {minutes} minutes"
            
        except Exception as e:
            logging.error(f"Error getting uptime: {e}")
            return "Unknown"
    
    def get_battery_info(self) -> Dict:
        """Get battery information (for laptops)"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percent': battery.percent,
                    'plugged_in': battery.power_plugged,
                    'time_left': str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
                }
            else:
                return {'error': 'No battery detected'}
                
        except Exception as e:
            logging.error(f"Error getting battery info: {e}")
            return {'error': str(e)}
    
    def generate_system_report(self) -> str:
        """Generate comprehensive system report"""
        try:
            report = []
            report.append("=" * 60)
            report.append("SHADOW AI SYSTEM DIAGNOSTICS REPORT")
            report.append("=" * 60)
            report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")
            
            # Basic system info
            report.append("SYSTEM INFORMATION:")
            report.append("-" * 30)
            sys_info = self.get_basic_system_info()
            for key, value in sys_info.items():
                report.append(f"{key.replace('_', ' ').title()}: {value}")
            report.append("")
            
            # CPU info
            report.append("CPU INFORMATION:")
            report.append("-" * 20)
            cpu_info = self.get_cpu_info()
            report.append(f"CPU Usage: {cpu_info.get('cpu_percent_total', 'N/A')}%")
            report.append(f"CPU Frequency: {cpu_info.get('cpu_frequency_current', 'N/A')} MHz")
            report.append("")
            
            # Memory info
            report.append("MEMORY INFORMATION:")
            report.append("-" * 25)
            mem_info = self.get_memory_info()
            report.append(f"Total Memory: {mem_info.get('total_gb', 'N/A')} GB")
            report.append(f"Used Memory: {mem_info.get('used_gb', 'N/A')} GB ({mem_info.get('percentage', 'N/A')}%)")
            report.append(f"Available Memory: {mem_info.get('available_gb', 'N/A')} GB")
            report.append("")
            
            # Disk info
            report.append("DISK INFORMATION:")
            report.append("-" * 20)
            disk_info = self.get_disk_info()
            for disk in disk_info:
                report.append(f"Drive {disk['device']}: {disk['used_gb']}/{disk['total_gb']} GB ({disk['percentage']}% used)")
            report.append("")
            
            # System health
            report.append("SYSTEM HEALTH CHECK:")
            report.append("-" * 25)
            health = self.check_system_health()
            report.append(f"Overall Status: {health.get('overall_status', 'Unknown')}")
            if health.get('warnings'):
                report.append("Warnings:")
                for warning in health['warnings']:
                    report.append(f"  - {warning}")
            if health.get('recommendations'):
                report.append("Recommendations:")
                for rec in health['recommendations']:
                    report.append(f"  - {rec}")
            report.append("")
            
            # Uptime
            report.append(f"System Uptime: {self.get_system_uptime()}")
            report.append("")
            
            # Top processes
            report.append("TOP PROCESSES (by CPU usage):")
            report.append("-" * 35)
            processes = self.get_running_processes(10)
            for proc in processes:
                report.append(f"{proc['name'][:20]:20} CPU: {proc.get('cpu_percent', 0):5.1f}% MEM: {proc.get('memory_mb', 0):6.1f}MB")
            
            report.append("=" * 60)
            
            return "\n".join(report)
            
        except Exception as e:
            logging.error(f"Error generating system report: {e}")
            return f"Error generating system report: {e}"

# Global instance
system_diagnostics = SystemDiagnostics()
