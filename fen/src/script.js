// 导入Three.js库和轨道控制器
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

// 定义粒子运动速度和轨迹长度的常量
const PARTICLE_SPEED = 0.05;
const MAX_TRAIL_LENGTH = 30;

// 初始化Three.js场景、相机和渲染器
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 添加轨道控制器，允许用户通过鼠标交互来旋转和缩放场景
const controls = new OrbitControls(camera, renderer.domElement);
camera.position.set(0, 0, 5);

// 创建坐标轴辅助线，帮助理解3D空间中的方向
const axesHelper = new THREE.AxesHelper(5)
scene.add(axesHelper)

// 创建五角星的形状
const starShape = new THREE.Shape();
const points = 5; // 五角星的顶点数
const outerRadius = 2; // 外圆半径
const innerRadius = outerRadius * 0.4; // 内圆半径（五角星凹陷部分）

// 通过数学计算绘制五角星的轮廓
for (let i = 0; i < points * 2; i++) {
  const radius = i % 2 === 0 ? outerRadius : innerRadius;
  const angle = (i * Math.PI) / points;
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;
  
  if (i === 0) {
    starShape.moveTo(x, y);
  } else {
    starShape.lineTo(x, y);
  }
}

starShape.closePath();

// 定义五角星的立体几何体参数
const extrudeSettings = {
  depth: 0.2, // 厚度
  bevelEnabled: true, // 启用斜角
  bevelThickness: 0.1, // 斜角厚度
  bevelSize: 0.1, // 斜角大小
  bevelSegments: 3 // 斜角分段数
};

// 创建五角星的立体几何体
const geometry = new THREE.ExtrudeGeometry(starShape, extrudeSettings);

// 创建金色材质，添加光泽效果
const material = new THREE.MeshPhongMaterial({
  color: 0xffd700, // 金色
  shininess: 100, // 光泽度
  specular: 0xffffff // 高光颜色
});

// 创建五角星网格并添加到场景
const star = new THREE.Mesh(geometry, material);
scene.add(star);

// 添加环境光和平行光源
const ambientLight = new THREE.AmbientLight(0x404040); // 柔和的环境光
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // 强烈的定向光
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);

// 计算五角星的包围盒尺寸，用于粒子系统的位置计算
const starBoundingBox = new THREE.Box3().setFromObject(star);
const starSize = new THREE.Vector3();
starBoundingBox.getSize(starSize);

// 在z轴正方向设置流体线发射器的位置
const fluidEmitterPosition = new THREE.Vector3(0, 0, 10);
const fluidParticles = []; // 存储所有流体线粒子

// 创建单个流体线粒子
function createFluidParticle() {
  // 创建粒子的几何体和材质
  const geometry = new THREE.BufferGeometry();
  const material = new THREE.LineBasicMaterial({
    color: '#ffffff',
    transparent: true,
    opacity: 0.4,
    side: THREE.DoubleSide,
  });
  
  // 计算粒子的随机初始位置
  const randomOffset = new THREE.Vector3(
    (Math.random() - 0.5) * starSize.x,
    (Math.random() - 0.5) * starSize.y,
    0
  );
  const position = fluidEmitterPosition.clone().add(randomOffset);
  
  // 创建粒子并设置其属性
  const particle = new THREE.Line(geometry, material);
  particle.userData = {
    trail: [position.clone()], // 粒子运动轨迹
    velocity: new THREE.Vector3(0, 0, -PARTICLE_SPEED), // 初始速度
    life: 2.0, // 生命周期
    isRotating: false, // 是否处于旋转状态
    rotationCount: 0 // 旋转圈数计数
  };
  
  scene.add(particle);
  fluidParticles.push(particle);
}

// 更新所有流体线粒子的状态
function updateFluidParticles() {
  // 每帧生成新的粒子
  createFluidParticle();
  
  // 更新现有粒子的位置和状态
  for (let i = fluidParticles.length - 1; i >= 0; i--) {
    const particle = fluidParticles[i];
    const trail = particle.userData.trail;
    const velocity = particle.userData.velocity;
    const currentPos = trail[trail.length - 1];
    
    // 检查粒子是否进入五角星的包围盒
    if (!particle.userData.isRotating && currentPos.z <= starBoundingBox.max.z && currentPos.z >= starBoundingBox.min.z
        && currentPos.x >= starBoundingBox.min.x && currentPos.x <= starBoundingBox.max.x
        && currentPos.y >= starBoundingBox.min.y && currentPos.y <= starBoundingBox.max.y) {
      particle.userData.isRotating = true;
    }
    
    // 处理粒子的旋转状态
    if (particle.userData.isRotating) {
      // 使粒子跟随五角星旋转
      velocity.applyAxisAngle(new THREE.Vector3(0, 0, 1), -0.02);
      particle.userData.rotationCount += 0.02 / (2 * Math.PI);
      
      // 完成指定圈数后恢复直线运动
      if (particle.userData.rotationCount >= 10) {
        particle.userData.isRotating = false;
        velocity.set(0, 0, -PARTICLE_SPEED);
      }
    }
    
    // 更新粒子位置
    const newPos = currentPos.clone().add(velocity);
    if (particle.userData.isRotating) {
      newPos.applyAxisAngle(new THREE.Vector3(0, 0, 1), -0.02);
    }
    trail.push(newPos);
    
    // 限制轨迹长度，保持固定数量的历史位置
    if (trail.length > MAX_TRAIL_LENGTH) {
      trail.shift();
    }
    
    // 更新粒子的几何体显示
    particle.geometry.setFromPoints(trail);
    
    // 检查粒子是否超出显示范围，如果是则移除
    if (newPos.z < -10) {
      scene.remove(particle);
      fluidParticles.splice(i, 1);
      continue;
    }
    
    // 保持粒子的透明度
    particle.material.opacity = 0.4;
  }
}

// 动画循环函数
function animate() {
  requestAnimationFrame(animate);
  
  // 使五角星绕z轴逆时针旋转
  star.rotation.z -= 0.02;
  
  // 更新流体线系统
  updateFluidParticles();
  
  // 渲染场景
  renderer.render(scene, camera);
}

// 启动动画循环
animate();

// 监听窗口大小变化，调整渲染尺寸
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

